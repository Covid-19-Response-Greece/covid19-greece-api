# this script downloads the data from https://github.com/Covid-19-Response-Greece/covid19-data-greece

import os
import urllib.request
import sys

DOWNLOADS_DIR = "./data/"


urls = [
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/all_countries/general/timeseries_per_country.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/general/timeseries_greece.json",
    # "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/isMOOD/daily-info.json",
    # "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/isMOOD/regions.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/regional/regions_history_cases.csv",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/regional/regions_history_deaths.csv",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/regional/regions_daily.csv",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/regional/regions_cumulative.csv",
    # "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/isMOOD/cases_by_region_timeline.csv",
    # "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/isMOOD/population_per_region.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/regional/western_macedonia_daily_reports.csv",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/regional/western_macedonia_deaths.csv",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/measures/greece_social_distancing_measures_timeline.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/refugee_camps/refugee_camps.csv",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/schools_status/covid19-schools.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/age_distribution/age_data.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/gender_distribution/gender_age_data.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/general/intensive_care_cases.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/general/tests.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/gender_distribution/female_cases_history.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/gender_distribution/male_cases_history.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/age_distribution/age_data_history.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/vaccines/vaccinations_data_history.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/vaccines/cumulative_per_area_vaccinations.json",
    "https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/data-restructuring/data/greece/vaccines/cumulative_vaccinations.json",
]

paths_to_store = [
    "all_countries/general",
    "greece/general",
    # "greece/isMOOD",
    # "greece/isMOOD",
    "greece/regional",
    "greece/regional",
    "greece/regional",
    "greece/regional",
    # "greece/isMOOD",
    # "greece/isMOOD",
    "greece/regional",
    "greece/regional",
    "greece/measures",
    "greece/refugee_camps",
    "greece/schools_status",
    "greece/age_distribution",
    "greece/gender_distribution",
    "greece/general",
    "greece/general",
    "greece/gender_distribution",
    "greece/gender_distribution",
    "greece/age_distribution",
    "greece/vaccines",
    "greece/vaccines",
    "greece/vaccines",
]


def download():
    print("Updating data ...")

    if not os.path.exists(DOWNLOADS_DIR):
        os.makedirs(DOWNLOADS_DIR)

    for i in range(0, len(urls)):
        url = urls[i]
        path = paths_to_store[i]

        name = url.rsplit("/", 1)[-1]
        filename = os.path.join(DOWNLOADS_DIR + path, name)

        try:
            urllib.request.urlretrieve(url, filename)
        except Exception as inst:
            print(inst)
            print("Encountered error at source number %d" % i)
            sys.exit()

    print("Done.")


if __name__ == "__main__":
    download()
