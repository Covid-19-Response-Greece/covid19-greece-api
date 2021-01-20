import json
import copy
import pandas as pd
import datetime

from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from flask import (
    Flask,
    jsonify,
    abort,
    make_response,
    send_from_directory,
    render_template
)


app = Flask(__name__)
cors = CORS(app)

data_greece_JHCSSE = None
data_greece_isMOOD_regions = None
data_greece_isMOOD_cases_region_timeline = None
data_greece_tests_npho = None
data_greece_intensive_care_npho = None
data_greece_age_dist_npho = None
data_greece_gender_age_dist_npho = None
# data_greece_wikipedia = None
data_greece_social_distancing_timeline = None
data_greece_refugee_camps = None
data_greece_regions_wm_deaths = None
data_greece_regions_wm = None
data_greece_regions_wm_deaths = None
data_greece_schools_status = None
population_per_region = None


def init():
    global data_greece_JHCSSE
    global data_greece_isMOOD_regions
    global data_greece_isMOOD_cases_region_timeline
    global data_greece_intensive_care_npho
    global data_greece_tests_npho
    global data_greece_age_dist_npho
    global data_greece_gender_age_dist_npho
    # global data_greece_wikipedia
    global data_greece_social_distancing_timeline
    global data_greece_refugee_camps
    global data_greece_regions_wm_deaths
    global data_greece_regions_wm
    global data_greece_regions_wm_deaths
    global data_greece_schools_status
    global population_per_region

    with open('data/greece/JohnsHopkinsCSSE/timeseries_greece.json') as f:
        data_greece_JHCSSE = json.load(f)['Greece']

    with open('data/greece/isMOOD/regions.json') as regions_file:
    	data_greece_isMOOD_regions = json.load(regions_file)

    with open('data/greece/isMOOD/cases_by_region_timeline.csv', encoding = 'utf-8') as f:
    	data_greece_isMOOD_cases_region_timeline = pd.read_csv(f)

    data_greece_isMOOD_cases_region_timeline = data_greece_isMOOD_cases_region_timeline.where(
        pd.notnull(data_greece_isMOOD_cases_region_timeline), None
    )

    with open('data/greece/NPHO/intensive_care_cases.json') as f:
        data_greece_intensive_care_npho = json.load(f)

    with open('data/greece/NPHO/tests.json') as f:
        data_greece_tests_npho = json.load(f)

    with open('data/greece/NPHO/age_data.json') as f:
        data_greece_age_dist_npho = json.load(f)

    with open('data/greece/NPHO/gender_age_data.json') as f:
        data_greece_gender_age_dist_npho = json.load(f)

    with open('data/greece/Measures/greece_social_distancing_measures_timeline.json', encoding = 'utf-8') as f:
        data_greece_social_distancing_timeline = json.load(f)

    with open('data/greece/Regions/western_macedonia_daily_reports.csv', encoding = 'utf-8') as f:
    	data_greece_regions_wm = pd.read_csv(f, date_parser=lambda x: datetime.datetime.strptime(x, '%d/%m/%Y'))

    data_greece_regions_wm = data_greece_regions_wm.where(pd.notnull(
        data_greece_regions_wm
    ), None)

    data_greece_regions_wm['Ημερομηνία Αναφοράς'] = pd.to_datetime(
        data_greece_regions_wm['Ημερομηνία Αναφοράς'], format='%d/%m/%Y'
    )

    data_greece_regions_wm = data_greece_regions_wm.sort_values(
        by=['Ημερομηνία Αναφοράς'], ascending=True
    )

    email_trust_list_wm = [
        'litsios.apo@gmail.com',
        'evpapadopoulos@gmail.com',
        'georkozari@gmail.com'
    ]

    data_greece_regions_wm = data_greece_regions_wm[
        data_greece_regions_wm['Διεύθυνση ηλεκτρονικού ταχυδρομείου'].isin(email_trust_list_wm)
    ]

    data_greece_regions_wm = data_greece_regions_wm.reset_index(drop = True)

    with open('data/greece/Regions/western_macedonia_deaths.csv', encoding = 'utf-8') as f:
        data_greece_regions_wm_deaths = pd.read_csv(f, date_parser=lambda x: datetime.datetime.strptime(x, '%d/%m/%Y'))

    with open('data/greece/Refugee_camps/refugee_camps.csv', encoding = 'utf-8') as f:
        data_greece_refugee_camps = pd.read_csv(f, date_parser=lambda x: datetime.datetime.strptime(x, '%d/%m/%Y'))

    data_greece_refugee_camps = data_greece_refugee_camps.where(pd.notnull(data_greece_refugee_camps), None)

    with open('data/greece/schools_status/covid19-schools.json', encoding = 'utf-8') as f:
        data_greece_schools_status = json.load(f)

    with open('data/greece/isMOOD/population_per_region.json') as f:
        population_per_region = json.load(f)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


SWAGGER_URL = '/docs'
API_URL = '/static/openapi.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name': 'Coronavirus Greece API',
        'layout': 'BaseLayout'
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix = SWAGGER_URL)


@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')


@app.route('/all', methods=['GET'])
def get_all():
    out_json = copy.deepcopy(data_greece_JHCSSE)

    for date in out_json:
        del date['recovered']

    return jsonify({'cases': out_json})


@app.route('/confirmed', methods=['GET'])
def get_confirmed():
    out_json = copy.deepcopy(data_greece_JHCSSE)

    for date in out_json:
        del date['recovered']
        del date['deaths']

    return jsonify({'cases': out_json})


@app.route('/recovered', methods=['GET'])
def get_recovered():
    out_json = copy.deepcopy(data_greece_JHCSSE)

    for date in out_json:
        del date['confirmed']
        del date['deaths']

    out_json = out_json[1:100]
    return jsonify({'cases': out_json})


@app.route('/deaths', methods=['GET'])
def get_deaths():
    out_json = copy.deepcopy(data_greece_JHCSSE)
    for date in out_json:
        del date['confirmed']
        del date['recovered']

    return jsonify({'cases': out_json})


@app.route('/regions', methods=['GET'])
def get_regions():
    out_json = copy.deepcopy(data_greece_isMOOD_regions)

    for region in out_json:
        region['population'] = None
        region['cases_per_100000_people'] = None

        for region_pop in population_per_region:

            if region['region_en_name'] == region_pop['region']:
                region['population'] = region_pop['population']

                region['cases_per_100000_people'] = round(
                    region['region_cases'] / region['population'] * 100000.0, 2
                )

    return jsonify({'regions': out_json})


@app.route('/regions-history', methods=['GET'])
def get_regions_history():
    region_gr_name = list(data_greece_isMOOD_cases_region_timeline['Περιφέρεια'])
    region_en_name = list(data_greece_isMOOD_cases_region_timeline['Region'])
    population = list(data_greece_isMOOD_cases_region_timeline['Population_2011'])
    dates = data_greece_isMOOD_cases_region_timeline.columns[3:]
    tot_json = []

    for date in dates:
        regions_cases = list(data_greece_isMOOD_cases_region_timeline[date])
        transformed_date = datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
        inner_json = []

        for reg_gr, reg_en, pop, reg_cases in zip(region_gr_name, region_en_name, population, regions_cases):
            region_data = {}
            region_data['region_gr_name'] = reg_gr
            region_data['region_en_name'] = reg_en
            region_data['population'] = int(pop) if pop!=None else None
            region_data['region_cases'] = reg_cases
            region_data['cases_per_100000_people'] = round(reg_cases / pop * 100000.0, 2) if pop!=None else None
            inner_json.append(region_data)

        outer_json = {}
        outer_json['date'] = transformed_date
        outer_json['regions'] = inner_json
        tot_json.append(outer_json)

    return jsonify({'regions-history': tot_json})


@app.route('/active', methods=['GET'])
def get_active():
    out_json = copy.deepcopy(data_greece_JHCSSE)

    for date in out_json:
        date['active'] = date['confirmed'] - date['deaths'] - date['recovered']
        del date['confirmed']
        del date['recovered']
        del date['deaths']

    out_json = out_json[1:100]
    return jsonify({'cases': out_json})


@app.route('/total', methods=['GET'])
def get_total():
    out_json = copy.deepcopy(data_greece_JHCSSE[-1])
    del out_json['recovered']
    return jsonify({'cases': out_json})


@app.route('/total-tests', methods=['GET'])
def get_total_tests():
    out_json = copy.deepcopy(data_greece_tests_npho)
    return jsonify(out_json)


@app.route('/intensive-care', methods=['GET'])
def get_intensive_care():
    out_json = copy.deepcopy(data_greece_intensive_care_npho)
    return jsonify(out_json)


@app.route('/gender-distribution', methods=['GET'])
def get_genders():
    out_json = copy.deepcopy(data_greece_gender_age_dist_npho)
    del out_json['total_age_groups']
    return jsonify({'gender_percentages': out_json})


@app.route('/age-distribution', methods=['GET'])
def get_age_groups():
    out_json = copy.deepcopy({'age_distribution': data_greece_age_dist_npho})
    return jsonify(out_json)


@app.route('/gender-age-distribution', methods=['GET'])
def get_gender_age_groups():
    out_json = copy.deepcopy(data_greece_gender_age_dist_npho)
    del out_json['total_females_percentage']
    del out_json['total_males_percentage']
    out_json['total_age_gender_distribution'] = out_json.pop('total_age_groups')
    return jsonify(out_json)


@app.route('/measures-timeline', methods=['GET'])
def get_measures_timeline():
    out_json = copy.deepcopy(data_greece_social_distancing_timeline)
    return jsonify({'measures': out_json})


@app.route('/western-macedonia', methods=['GET'])
def get_western_macedonia():

    hospitals = [
        'geniko_kozanis_mamatseio',
        'geniko_ptolemaidas_mpodosakeio',
        'geniko_kastorias',
        'geniko_flwrinas_dimitriou',
        'geniko_grevenwn'
    ]

    tot_json = []

    for i, row in data_greece_regions_wm.iterrows():
        date = row['Ημερομηνία Αναφοράς']

        transformed_date = datetime.datetime.strptime(
            str(date), '%Y-%m-%d %H:%M:%S'
        ).strftime('%Y-%m-%d')

        inner_json = []
        k = 7 # standard length of hospital info (excluding name)

        for i in range(len(hospitals)):
            hospital_data = {}
            hospital_data['hospital_name'] = hospitals[i]
            hospital_data['new_samples'] = row.iloc[i*k+3]
            hospital_data['hospitalized_current'] = row.iloc[i*k+4]
            hospital_data['hospitalized_positive'] = row.iloc[i*k+5]
            hospital_data['hospitalized_negative'] = row.iloc[i*k+6]
            hospital_data['hospitalized_pending_result'] = row.iloc[i*k+7]
            hospital_data['new_recoveries'] = row.iloc[i*k+8]
            hospital_data['home_restriction_current'] = row.iloc[i*k+9]

            inner_json.append(hospital_data)

        total = {}
        total['hospitalized_ICU_current'] = row['Νοσηλευόμενοι σε ΜΕΘ (Τρέχων Αριθμός - Μποδοσάκειο)']
        total['total_samples'] = row['Συνολικοί Έλεγχοι Δειγμάτων']
        total['total_samples_positive'] = row['Συνολικά Θετικά Δείγματα']
        total['total_samples_negative'] = row['Συνολικά Αρνητικά Δείγματα']
        total['total_deaths'] = row['Συνολικοί Θάνατοι']

        outer_json = {}
        outer_json['date'] = transformed_date
        outer_json['hospitals'] = inner_json
        outer_json['total'] = total
        tot_json.append(outer_json)

    return jsonify({'western-macedonia': tot_json})

@app.route('/western-macedonia-deaths', methods=['GET'])
def get_western_macedonia_deaths():
    sex_dict = {'Άνδρας':'male', 'Γυναίκα':'female'}
    underlying_diseases_dict = {'Ναι':'yes', 'Όχι':'no', 'Άγνωστο':'unkwown'}

    municipality_dict = {
        'ΔΗΜΟΣ ΓΡΕΒΕΝΩΝ': 'dimos_grevenon',
        'ΔΗΜΟΣ ΔΕΣΚΑΤΗΣ': 'dimos_deskatis',
        'ΔΗΜΟΣ ΚΑΣΤΟΡΙΑΣ': 'dimos_kastorias',
        'ΔΗΜΟΣ ΝΕΣΤΟΡΙΟΥ': 'dimos_nestoriou',
        'ΔΗΜΟΣ ΟΡΕΣΤΙΔΟΣ': 'dimos_orestidos',
        'ΔΗΜΟΣ ΒΟΪΟΥ': 'dimos_voiou',
        'ΔΗΜΟΣ ΕΟΡΔΑΙΑΣ': 'dimos_eordaias',
        'ΔΗΜΟΣ ΚΟΖΑΝΗΣ': 'dimos_kozanis',
        'ΔΗΜΟΣ ΣΕΡΒΙΩΝ': 'dimos_servion',
        'ΔΗΜΟΣ ΒΕΛΒΕΝΤΟΥ':'dimos_velventou',
        'ΔΗΜΟΣ ΑΜΥΝΤΑΙΟΥ': 'dimos_amintaiou',
        'ΔΗΜΟΣ ΠΡΕΣΠΩΝ': 'dimos_prespon',
        'ΔΗΜΟΣ ΦΛΩΡΙΝΑΣ': 'dimos_florinas'
    }

    tot_json = []

    for i, row in data_greece_regions_wm_deaths.iterrows():
        transformed_date = datetime.datetime.strptime(row['Ημερομηνία Αναφοράς Θανάτου'], '%d/%m/%Y').strftime('%Y-%m-%d')
        out_json = {}
        out_json['date'] = transformed_date
        out_json['age'] = row['Ηλικία']
        out_json['sex'] = sex_dict[row['Φύλο']]
        out_json['underlying_diseases'] = underlying_diseases_dict[row['Υποκείμενα Νοσήματα']]
        out_json['permanent_residence_municipality_gr'] = row['Δήμος Μόνιμης Κατοικίας']
        out_json['permanent_residence_municipality_en'] = municipality_dict[row['Δήμος Μόνιμης Κατοικίας']]
        tot_json.append(out_json)

    return jsonify({'western-macedonia-deaths': tot_json})


@app.route('/refugee-camps', methods=['GET'])
def get_refugee_camps():
    area_type_dict = {'Ηπειρωτική':'mainland', 'Νησιωτική':'island'}

    region_dict = {
        'Ανατολικής Μακεδονίας και Θράκης': 'Eastern Macedonia and Thrace',
        'Αττικής': 'Attica',
        'Βορείου Αιγαίου': 'North Aegean',
        'Δυτικής Ελλάδας': 'Western Greece',
        'Δυτικής Μακεδονίας': 'Western Macedonia',
        'Ηπείρου': 'Epirus',
        'Θεσσαλίας': 'Thessaly',
        'Ιονίων Νήσων': 'Ionian Islands',
        'Κεντρικής Μακεδονίας': 'Central Macedonia',
        'Κρήτης': 'Crete',
        'Νοτίου Αιγαίου': 'South Aegean',
        'Πελλοπονήσου': 'Peloponnese',
        'Στερεάς Ελλάδας': 'Central Greece'
    }

    tot_json = []

    for i, row in data_greece_refugee_camps.iterrows():

        if row['Όνομα Δομής'] != None :
            camp_data = {}
            camp_data['name_gr'] = row['Όνομα Δομής']
            camp_data['name_en'] = row['Refugee Camp Name']
            camp_data['region_gr'] = row['Περιφέρεια']
            camp_data['region_en'] = region_dict[row['Περιφέρεια']]
            camp_data['description'] = row['Περιγραφή Δομής']
            camp_data['capacity'] = int(row['Χωρητικότητα']) if row['Χωρητικότητα'] != None else None
            camp_data['current_hosts'] = int(row['Αριθμός Φιλοξενούμενων']) if row['Αριθμός Φιλοξενούμενων'] != None else None
            camp_data['area_type_gr'] = row['Έκταση']
            camp_data['area_type_en'] = area_type_dict[row['Έκταση']]
            camp_data['longtitude'] = float(row['Γεωγραφικό Μήκος'].replace(',','.')) if row['Γεωγραφικό Μήκος'] != None else None
            camp_data['latitude'] =  float(row['Γεωγραφικό Πλάτος'].replace(',','.')) if row['Γεωγραφικό Πλάτος'] != None else None
            camp_data['last update'] = datetime.datetime.strptime(row['Τελευταία Ενημέρωση'], '%d/%m/%Y').strftime('%Y-%m-%d')
            camp_data['total_confirmed_cases'] = 0
            camp_data['total_samples'] = 0
            recorded_events = []

            k = 0

            inner_json = {}
            inner_json['confirmed_cases'] = int(data_greece_refugee_camps.iloc[i+k, 10]) if data_greece_refugee_camps.iloc[i+k, 10] != None else None
            if inner_json['confirmed_cases'] != None:
                camp_data['total_confirmed_cases'] += inner_json['confirmed_cases']

            inner_json['samples'] = int(data_greece_refugee_camps.iloc[i+k, 11]) if data_greece_refugee_camps.iloc[i+k, 11] != None else None
            if inner_json['samples'] != None: camp_data['total_samples'] += inner_json['samples']

            inner_json['case_detection_week'] = data_greece_refugee_camps.iloc[i+k, 12]
            inner_json['quarantine_duration_days'] = int(data_greece_refugee_camps.iloc[i+k, 13]) if data_greece_refugee_camps.iloc[i+k, 13]!= None else None
            recorded_events.append(inner_json)

            k += 1

            while data_greece_refugee_camps.iloc[i+k, 0] == None:

                inner_json = {}
                inner_json['confirmed_cases'] = int(data_greece_refugee_camps.iloc[i+k, 10]) if data_greece_refugee_camps.iloc[i+k, 10] != None else None
                if inner_json['confirmed_cases'] != None: camp_data['total_confirmed_cases'] += inner_json['confirmed_cases']

                inner_json['samples'] = int(data_greece_refugee_camps.iloc[i+k, 11]) if data_greece_refugee_camps.iloc[i+k, 11] != None else None
                if inner_json['samples'] != None: camp_data['total_samples'] += inner_json['samples']
                inner_json['case_detection_week'] = data_greece_refugee_camps.iloc[i+k, 12]
                inner_json['quarantine_duration_days'] = int(data_greece_refugee_camps.iloc[i+k, 13]) if data_greece_refugee_camps.iloc[i+k, 13] != None else None

                recorded_events.append(inner_json)
                k += 1

                if i+k >= len(data_greece_refugee_camps):
                    break

            camp_data['recorded_events'] = recorded_events
            tot_json.append(camp_data)

        else:
            continue

    return jsonify({'refugee-camps': tot_json})


@app.route('/schools-status', methods=['GET'])
def get_schools_status():

    out_json = copy.deepcopy(data_greece_schools_status)

    return jsonify({'schools-status': out_json})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


init()

if __name__ == '__main__':
    app.run()
