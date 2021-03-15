import json
import copy
import pandas as pd
import datetime

# from datetime import  timedelta
import numpy as np

from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from flask import (
    Flask,
    jsonify,
    abort,
    make_response,
    send_from_directory,
    render_template,
)


app = Flask(__name__)
cors = CORS(app)

data_greece_general = None
# data_greece_isMOOD_regions = None
# data_greece_isMOOD_cases_region_timeline = None
data_greece_regions_history = None
data_greece_regions_cumulative = None
data_greece_tests_npho = None
data_greece_intensive_care_npho = None
data_greece_age_dist_npho = None
data_greece_gender_age_dist_npho = None
# data_greece_wikipedia = None
data_greece_social_distancing_timeline = None
data_greece_risk_levels = None
data_greece_social_distancing_measures_by_risk_level = None
data_greece_refugee_camps = None
data_greece_regions_wm_deaths = None
data_greece_regions_wm = None
data_greece_regions_wm_deaths = None
data_greece_schools_status = None
# population_per_region = None
data_greece_male_cases = None
data_greece_female_cases = None
data_greece_age_data = None
vaccinations_data_history = None
cumulative_vaccinations_data = None
cumulative_per_area_vaccinations_data = None


def init():
    global data_greece_general
    # global data_greece_isMOOD_regions
    # global data_greece_isMOOD_cases_region_timeline
    global data_greece_regions_history
    global data_greece_regions_cumulative
    global data_greece_intensive_care_npho
    global data_greece_tests_npho
    global data_greece_age_dist_npho
    global data_greece_gender_age_dist_npho
    # global data_greece_wikipedia
    global data_greece_social_distancing_timeline
    global data_greece_risk_levels
    global data_greece_social_distancing_measures_by_risk_level
    global data_greece_refugee_camps
    global data_greece_regions_wm_deaths
    global data_greece_regions_wm
    global data_greece_regions_wm_deaths
    global data_greece_schools_status
    # global population_per_region
    global data_greece_male_cases
    global data_greece_female_cases
    global data_greece_age_data
    global vaccinations_data_history
    global cumulative_vaccinations_data
    global cumulative_per_area_vaccinations_data

    with open("data/greece/general/timeseries_greece.json") as f:
        data_greece_general = json.load(f)["Greece"]

    # with open('data/greece/isMOOD/regions.json') as regions_file:
    #     data_greece_isMOOD_regions = json.load(regions_file)

    # with open('data/greece/isMOOD/cases_by_region_timeline.csv', encoding='utf-8') as f:
    #     data_greece_isMOOD_cases_region_timeline = pd.read_csv(f)

    # data_greece_isMOOD_cases_region_timeline = data_greece_isMOOD_cases_region_timeline.where(
    #     pd.notnull(data_greece_isMOOD_cases_region_timeline), None
    # )

    with open(
        "data/greece/regional/regions_history_cases.json",
        encoding="utf-8",
    ) as f:
        data_greece_regions_history = json.load(f)

    with open("data/greece/regional/regions_cumulative.csv", encoding="utf-8") as f:
        data_greece_regions_cumulative = pd.read_csv(f)

    data_greece_regions_cumulative = data_greece_regions_cumulative.drop(
        columns=["total_deaths"]
    )
    data_greece_regions_cumulative = data_greece_regions_cumulative.where(
        pd.notnull(data_greece_regions_cumulative), None
    )

    with open("data/greece/general/intensive_care_cases.json") as f:
        data_greece_intensive_care_npho = json.load(f)

    with open("data/greece/general/tests.json") as f:
        data_greece_tests_npho = json.load(f)

    with open("data/greece/age_distribution/age_data.json") as f:
        data_greece_age_dist_npho = json.load(f)

    with open("data/greece/gender_distribution/gender_age_data.json") as f:
        data_greece_gender_age_dist_npho = json.load(f)

    with open(
        "data/greece/measures/greece_social_distancing_measures_timeline.json",
        encoding="utf-8",
    ) as f:
        data_greece_social_distancing_timeline = json.load(f)
    
    with open(
        "data/greece/measures/greece_risk_levels.json",
        encoding="utf-8",
    ) as f:
        data_greece_risk_levels = json.load(f)
    
    with open(
        "data/greece/measures/greece_social_distancing_measures_by_risk_level.json",
        encoding="utf-8",
    ) as f:
        data_greece_social_distancing_measures_by_risk_level = json.load(f)

    with open(
        "data/greece/regional/western_macedonia_daily_reports.csv", encoding="utf-8"
    ) as f:
        data_greece_regions_wm = pd.read_csv(
            f, date_parser=lambda x: datetime.datetime.strptime(x, "%d/%m/%Y")
        )

    data_greece_regions_wm = data_greece_regions_wm.where(
        pd.notnull(data_greece_regions_wm), None
    )

    data_greece_regions_wm["Ημερομηνία Αναφοράς"] = pd.to_datetime(
        data_greece_regions_wm["Ημερομηνία Αναφοράς"], format="%d/%m/%Y"
    )

    data_greece_regions_wm = data_greece_regions_wm.sort_values(
        by=["Ημερομηνία Αναφοράς"], ascending=True
    )

    email_trust_list_wm = [
        "litsios.apo@gmail.com",
        "evpapadopoulos@gmail.com",
        "georkozari@gmail.com",
    ]

    data_greece_regions_wm = data_greece_regions_wm[
        data_greece_regions_wm["Διεύθυνση ηλεκτρονικού ταχυδρομείου"].isin(
            email_trust_list_wm
        )
    ]

    data_greece_regions_wm = data_greece_regions_wm.reset_index(drop=True)

    with open(
        "data/greece/regional/western_macedonia_deaths.csv", encoding="utf-8"
    ) as f:
        data_greece_regions_wm_deaths = pd.read_csv(
            f, date_parser=lambda x: datetime.datetime.strptime(x, "%d/%m/%Y")
        )

    with open("data/greece/refugee_camps/refugee_camps.csv", encoding="utf-8") as f:
        data_greece_refugee_camps = pd.read_csv(
            f, date_parser=lambda x: datetime.datetime.strptime(x, "%d/%m/%Y")
        )

    data_greece_refugee_camps = data_greece_refugee_camps.where(
        pd.notnull(data_greece_refugee_camps), None
    )

    with open("data/greece/schools_status/covid19-schools.json", encoding="utf-8") as f:
        data_greece_schools_status = json.load(f)

    # with open("data/greece/isMOOD/population_per_region.json") as f:
    #     population_per_region = json.load(f)

    with open(
        "data/greece/gender_distribution/male_cases_history.json", encoding="utf-8"
    ) as f:
        data_greece_male_cases = json.load(f)

    with open(
        "data/greece/gender_distribution/female_cases_history.json", encoding="utf-8"
    ) as f:
        data_greece_female_cases = json.load(f)

    with open(
        "data/greece/age_distribution/age_data_history.json", encoding="utf-8"
    ) as f:
        data_greece_age_data = json.load(f)

    with open(
        "data/greece/vaccines/vaccinations_data_history.json", encoding="utf-8"
    ) as f:
        vaccinations_data_history = json.load(f)

    with open(
        "data/greece/vaccines/cumulative_per_area_vaccinations.json", encoding="utf-8"
    ) as f:
        cumulative_per_area_vaccinations_data = json.load(f)

    with open(
        "data/greece/vaccines/cumulative_vaccinations.json", encoding="utf-8"
    ) as f:
        cumulative_vaccinations_data = json.load(f)


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


SWAGGER_URL = "/docs"
API_URL = "/static/openapi.json"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Coronavirus Greece API", "layout": "BaseLayout"},
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route("/", methods=["GET"])
def get_index():
    return render_template("index.html")


@app.route("/all", methods=["GET"])
def get_all():
    out_json = copy.deepcopy(data_greece_general)

    for date in out_json:
        del date["recovered"]

    return jsonify({"cases": out_json})


@app.route("/confirmed", methods=["GET"])
def get_confirmed():
    out_json = copy.deepcopy(data_greece_general)

    for date in out_json:
        del date["recovered"]
        del date["deaths"]

    return jsonify({"cases": out_json})


@app.route("/recovered", methods=["GET"])
def get_recovered():
    out_json = copy.deepcopy(data_greece_general)

    for date in out_json:
        del date["confirmed"]
        del date["deaths"]

    out_json = out_json[1:100]
    return jsonify({"cases": out_json})


@app.route("/deaths", methods=["GET"])
def get_deaths():
    out_json = copy.deepcopy(data_greece_general)
    for date in out_json:
        del date["confirmed"]
        del date["recovered"]

    return jsonify({"cases": out_json})


@app.route("/regions", methods=["GET"])
def get_regions():
    out_json = []

    for i, row in data_greece_regions_cumulative.iterrows():
        region_cases = {}
        region_cases = dict(row)
        region_cases["cases_per_100000_people"] = (
            round(row["total_cases"] / row["population"] * 100000.0, 2)
            if (row["population"] != None and row["total_cases"] != None)
            else None
        )
        out_json.append(region_cases)

    return jsonify({"regions": out_json})


@app.route("/regions-history", methods=["GET"])
def get_regions_history():

    out_json = copy.deepcopy(data_greece_regions_history)

    return jsonify({"regions-history": out_json})


@app.route("/active", methods=["GET"])
def get_active():
    out_json = copy.deepcopy(data_greece_general)

    for date in out_json:
        date["active"] = date["confirmed"] - date["deaths"] - date["recovered"]
        del date["confirmed"]
        del date["recovered"]
        del date["deaths"]

    out_json = out_json[1:100]
    return jsonify({"cases": out_json})


@app.route("/total", methods=["GET"])
def get_total():
    out_json = copy.deepcopy(data_greece_general[-1])
    del out_json["recovered"]
    return jsonify({"cases": out_json})


@app.route("/total-tests", methods=["GET"])
def get_total_tests():
    out_json = copy.deepcopy(data_greece_tests_npho)
    return jsonify(out_json)


@app.route("/intensive-care", methods=["GET"])
def get_intensive_care():
    out_json = copy.deepcopy(data_greece_intensive_care_npho)
    return jsonify(out_json)


@app.route("/gender-distribution", methods=["GET"])
def get_genders():
    out_json = copy.deepcopy(data_greece_gender_age_dist_npho)
    del out_json["total_age_groups"]
    return jsonify({"gender_percentages": out_json})


@app.route("/age-distribution", methods=["GET"])
def get_age_groups():
    out_json = copy.deepcopy({"age_distribution": data_greece_age_dist_npho})
    return jsonify(out_json)


@app.route("/gender-age-distribution", methods=["GET"])
def get_gender_age_groups():
    out_json = copy.deepcopy(data_greece_gender_age_dist_npho)
    del out_json["total_females_percentage"]
    del out_json["total_males_percentage"]
    out_json["total_age_gender_distribution"] = out_json.pop("total_age_groups")
    return jsonify(out_json)


@app.route("/measures-timeline", methods=["GET"])
def get_measures_timeline():
    out_json = copy.deepcopy(data_greece_social_distancing_timeline)
    return jsonify({"measures": out_json})


@app.route("/risk-levels", methods=["GET"])
def get_risk_levels():
    out_json = copy.deepcopy(data_greece_risk_levels)
    return jsonify({"risk_levels": out_json})


@app.route("/measures-by-risk-level", methods=["GET"])
def get_measures_by_risk_level():
    out_json = copy.deepcopy(data_greece_social_distancing_measures_by_risk_level)
    return jsonify({"measures_by_risk_level": out_json})


@app.route("/western-macedonia", methods=["GET"])
def get_western_macedonia():

    hospitals = [
        "geniko_kozanis_mamatseio",
        "geniko_ptolemaidas_mpodosakeio",
        "geniko_kastorias",
        "geniko_flwrinas_dimitriou",
        "geniko_grevenwn",
    ]

    tot_json = []

    for i, row in data_greece_regions_wm.iterrows():
        date = row["Ημερομηνία Αναφοράς"]

        transformed_date = datetime.datetime.strptime(
            str(date), "%Y-%m-%d %H:%M:%S"
        ).strftime("%Y-%m-%d")

        inner_json = []
        k = 7  # standard length of hospital info (excluding name)

        for i in range(len(hospitals)):
            hospital_data = {}
            hospital_data["hospital_name"] = hospitals[i]
            hospital_data["new_samples"] = row.iloc[i * k + 3]
            hospital_data["hospitalized_current"] = row.iloc[i * k + 4]
            hospital_data["hospitalized_positive"] = row.iloc[i * k + 5]
            hospital_data["hospitalized_negative"] = row.iloc[i * k + 6]
            hospital_data["hospitalized_pending_result"] = row.iloc[i * k + 7]
            hospital_data["new_recoveries"] = row.iloc[i * k + 8]
            hospital_data["home_restriction_current"] = row.iloc[i * k + 9]

            inner_json.append(hospital_data)

        total = {}
        total["hospitalized_ICU_current"] = row[
            "Νοσηλευόμενοι σε ΜΕΘ (Τρέχων Αριθμός - Μποδοσάκειο)"
        ]
        total["total_samples"] = row["Συνολικοί Έλεγχοι Δειγμάτων"]
        total["total_samples_positive"] = row["Συνολικά Θετικά Δείγματα"]
        total["total_samples_negative"] = row["Συνολικά Αρνητικά Δείγματα"]
        total["total_deaths"] = row["Συνολικοί Θάνατοι"]

        outer_json = {}
        outer_json["date"] = transformed_date
        outer_json["hospitals"] = inner_json
        outer_json["total"] = total
        tot_json.append(outer_json)

    return jsonify({"western-macedonia": tot_json})


@app.route("/western-macedonia-deaths", methods=["GET"])
def get_western_macedonia_deaths():
    sex_dict = {"Άνδρας": "male", "Γυναίκα": "female"}
    underlying_diseases_dict = {"Ναι": "yes", "Όχι": "no", "Άγνωστο": "unkwown"}

    municipality_dict = {
        "ΔΗΜΟΣ ΓΡΕΒΕΝΩΝ": "dimos_grevenon",
        "ΔΗΜΟΣ ΔΕΣΚΑΤΗΣ": "dimos_deskatis",
        "ΔΗΜΟΣ ΚΑΣΤΟΡΙΑΣ": "dimos_kastorias",
        "ΔΗΜΟΣ ΝΕΣΤΟΡΙΟΥ": "dimos_nestoriou",
        "ΔΗΜΟΣ ΟΡΕΣΤΙΔΟΣ": "dimos_orestidos",
        "ΔΗΜΟΣ ΒΟΪΟΥ": "dimos_voiou",
        "ΔΗΜΟΣ ΕΟΡΔΑΙΑΣ": "dimos_eordaias",
        "ΔΗΜΟΣ ΚΟΖΑΝΗΣ": "dimos_kozanis",
        "ΔΗΜΟΣ ΣΕΡΒΙΩΝ": "dimos_servion",
        "ΔΗΜΟΣ ΒΕΛΒΕΝΤΟΥ": "dimos_velventou",
        "ΔΗΜΟΣ ΑΜΥΝΤΑΙΟΥ": "dimos_amintaiou",
        "ΔΗΜΟΣ ΠΡΕΣΠΩΝ": "dimos_prespon",
        "ΔΗΜΟΣ ΦΛΩΡΙΝΑΣ": "dimos_florinas",
    }

    tot_json = []

    for i, row in data_greece_regions_wm_deaths.iterrows():
        transformed_date = datetime.datetime.strptime(
            row["Ημερομηνία Αναφοράς Θανάτου"], "%d/%m/%Y"
        ).strftime("%Y-%m-%d")
        out_json = {}
        out_json["date"] = transformed_date
        out_json["age"] = row["Ηλικία"]
        out_json["sex"] = sex_dict[row["Φύλο"]]
        out_json["underlying_diseases"] = underlying_diseases_dict[
            row["Υποκείμενα Νοσήματα"]
        ]
        out_json["permanent_residence_municipality_gr"] = row["Δήμος Μόνιμης Κατοικίας"]
        out_json["permanent_residence_municipality_en"] = municipality_dict[
            row["Δήμος Μόνιμης Κατοικίας"]
        ]
        tot_json.append(out_json)

    return jsonify({"western-macedonia-deaths": tot_json})


@app.route("/refugee-camps", methods=["GET"])
def get_refugee_camps():
    area_type_dict = {"Ηπειρωτική": "mainland", "Νησιωτική": "island"}

    region_dict = {
        "Ανατολικής Μακεδονίας και Θράκης": "Eastern Macedonia and Thrace",
        "Αττικής": "Attica",
        "Βορείου Αιγαίου": "North Aegean",
        "Δυτικής Ελλάδας": "Western Greece",
        "Δυτικής Μακεδονίας": "Western Macedonia",
        "Ηπείρου": "Epirus",
        "Θεσσαλίας": "Thessaly",
        "Ιονίων Νήσων": "Ionian Islands",
        "Κεντρικής Μακεδονίας": "Central Macedonia",
        "Κρήτης": "Crete",
        "Νοτίου Αιγαίου": "South Aegean",
        "Πελλοπονήσου": "Peloponnese",
        "Στερεάς Ελλάδας": "Central Greece",
    }

    tot_json = []

    for i, row in data_greece_refugee_camps.iterrows():

        if row["Όνομα Δομής"] != None:
            camp_data = {}
            camp_data["name_gr"] = row["Όνομα Δομής"]
            camp_data["name_en"] = row["Refugee Camp Name"]
            camp_data["region_gr"] = row["Περιφέρεια"]
            camp_data["region_en"] = region_dict[row["Περιφέρεια"]]
            camp_data["description"] = row["Περιγραφή Δομής"]
            camp_data["capacity"] = (
                int(row["Χωρητικότητα"]) if row["Χωρητικότητα"] != None else None
            )
            camp_data["current_hosts"] = (
                int(row["Αριθμός Φιλοξενούμενων"])
                if row["Αριθμός Φιλοξενούμενων"] != None
                else None
            )
            camp_data["area_type_gr"] = row["Έκταση"]
            camp_data["area_type_en"] = area_type_dict[row["Έκταση"]]
            camp_data["longtitude"] = (
                float(row["Γεωγραφικό Μήκος"].replace(",", "."))
                if row["Γεωγραφικό Μήκος"] != None
                else None
            )
            camp_data["latitude"] = (
                float(row["Γεωγραφικό Πλάτος"].replace(",", "."))
                if row["Γεωγραφικό Πλάτος"] != None
                else None
            )
            camp_data["last update"] = datetime.datetime.strptime(
                row["Τελευταία Ενημέρωση"], "%d/%m/%Y"
            ).strftime("%Y-%m-%d")
            camp_data["total_confirmed_cases"] = 0
            camp_data["total_samples"] = 0
            recorded_events = []

            k = 0

            inner_json = {}
            inner_json["confirmed_cases"] = (
                int(data_greece_refugee_camps.iloc[i + k, 10])
                if data_greece_refugee_camps.iloc[i + k, 10] != None
                else None
            )
            if inner_json["confirmed_cases"] != None:
                camp_data["total_confirmed_cases"] += inner_json["confirmed_cases"]

            inner_json["samples"] = (
                int(data_greece_refugee_camps.iloc[i + k, 11])
                if data_greece_refugee_camps.iloc[i + k, 11] != None
                else None
            )
            if inner_json["samples"] != None:
                camp_data["total_samples"] += inner_json["samples"]

            inner_json["case_detection_week"] = data_greece_refugee_camps.iloc[
                i + k, 12
            ]
            inner_json["quarantine_duration_days"] = (
                int(data_greece_refugee_camps.iloc[i + k, 13])
                if data_greece_refugee_camps.iloc[i + k, 13] != None
                else None
            )
            recorded_events.append(inner_json)

            k += 1

            while data_greece_refugee_camps.iloc[i + k, 0] == None:

                inner_json = {}
                inner_json["confirmed_cases"] = (
                    int(data_greece_refugee_camps.iloc[i + k, 10])
                    if data_greece_refugee_camps.iloc[i + k, 10] != None
                    else None
                )
                if inner_json["confirmed_cases"] != None:
                    camp_data["total_confirmed_cases"] += inner_json["confirmed_cases"]

                inner_json["samples"] = (
                    int(data_greece_refugee_camps.iloc[i + k, 11])
                    if data_greece_refugee_camps.iloc[i + k, 11] != None
                    else None
                )
                if inner_json["samples"] != None:
                    camp_data["total_samples"] += inner_json["samples"]
                inner_json["case_detection_week"] = data_greece_refugee_camps.iloc[
                    i + k, 12
                ]
                inner_json["quarantine_duration_days"] = (
                    int(data_greece_refugee_camps.iloc[i + k, 13])
                    if data_greece_refugee_camps.iloc[i + k, 13] != None
                    else None
                )

                recorded_events.append(inner_json)
                k += 1

                if i + k >= len(data_greece_refugee_camps):
                    break

            camp_data["recorded_events"] = recorded_events
            tot_json.append(camp_data)

        else:
            continue

    return jsonify({"refugee-camps": tot_json})


@app.route("/schools-status", methods=["GET"])
def get_schools_status():

    out_json = copy.deepcopy(data_greece_schools_status)

    return jsonify({"schools-status": out_json})


@app.route("/age-distribution-history", methods=["GET"])
def get_age_distribution_history():

    out_json = copy.deepcopy(data_greece_age_data)

    return jsonify({"age-distribution": out_json})


@app.route("/male-cases-history", methods=["GET"])
def get_male_cases_history():

    out_json = copy.deepcopy(data_greece_male_cases)

    return jsonify({"male-cases": out_json})


@app.route("/female-cases-history", methods=["GET"])
def get_female_cases_history():

    out_json = copy.deepcopy(data_greece_female_cases)

    return jsonify({"female-cases": out_json})


@app.route("/vaccinations-per-region-history", methods=["GET"])
def get_vaccinations_per_region_history():

    out_json = copy.deepcopy(vaccinations_data_history)

    return jsonify({"vaccinations-history": out_json})


@app.route("/total-vaccinations-per-region", methods=["GET"])
def get_total_vaccinations_per_region():

    out_json = copy.deepcopy(cumulative_per_area_vaccinations_data)

    return jsonify({"total-vaccinations": out_json})


@app.route("/total-vaccinations", methods=["GET"])
def get_total_vaccinations():

    out_json = copy.deepcopy(cumulative_vaccinations_data)

    return jsonify({"total-vaccinations": out_json})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


init()

if __name__ == "__main__":
    app.run()
