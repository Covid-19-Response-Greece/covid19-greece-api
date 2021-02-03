# this script downloads the data from https://github.com/Covid-19-Response-Greece/covid19-data-greece

import os
import urllib.request
import sys

DOWNLOADS_DIR = './data/'


urls = [
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/all_countries/JohnsHopkinsCSSE/cleaned-data/timeseries_per_country.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/JohnsHopkinsCSSE/timeseries_greece.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/isMOOD/daily-info.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/isMOOD/regions.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/iMEdD-Lab/regions_history_cases.csv',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/iMEdD-Lab/regions_history_deaths.csv',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/iMEdD-Lab/regions_daily.csv',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/iMEdD-Lab/regions_cumulative.csv',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/isMOOD/cases_by_region_timeline.csv',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/isMOOD/population_per_region.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/Regions/western_macedonia_daily_reports.csv',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/Regions/western_macedonia_deaths.csv',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/Measures/greece_social_distancing_measures_timeline.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/Refugee_camps/refugee_camps.csv',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/schools_status/covid19-schools.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/NPHO/age_data.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/NPHO/gender_age_data.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/NPHO/intensive_care_cases.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/NPHO/tests.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/NPHO/female_cases_history.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/NPHO/male_cases_history.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/NPHO/age_data_history.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/NPHO/vaccinations_data_history.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/NPHO/cumulative_per_area_vaccinations.json',
    'https://raw.githubusercontent.com/Covid-19-Response-Greece/covid19-data-greece/master/data/greece/NPHO/cumulative_vaccinations.json'
]

paths_to_store = [
    'all_countries/JohnsHopkinsCSSE',
    'greece/JohnsHopkinsCSSE',
    'greece/isMOOD',
    'greece/isMOOD',
    'greece/iMEdD-Lab',
    'greece/iMEdD-Lab',
    'greece/iMEdD-Lab',
    'greece/iMEdD-Lab',
    'greece/isMOOD',
    'greece/isMOOD',
    'greece/Regions',
    'greece/Regions',
    'greece/Measures',
    'greece/Refugee_camps',
    'greece/schools_status',
    'greece/NPHO',
    'greece/NPHO',
    'greece/NPHO',
    'greece/NPHO',
    'greece/NPHO',
    'greece/NPHO',
    'greece/NPHO',
    'greece/NPHO',
    'greece/NPHO',
    'greece/NPHO'
]


def download():
    print('Updating data ...')

    if not os.path.exists(DOWNLOADS_DIR):
        os.makedirs(DOWNLOADS_DIR)

    for i in range(0, len(urls)):
        url = urls[i]
        path = paths_to_store[i]

        name = url.rsplit('/', 1)[-1]
        filename = os.path.join(DOWNLOADS_DIR + path, name)

        try:
            urllib.request.urlretrieve(url, filename)
        except Exception as inst:
            print(inst)
            print('Encountered error')
            sys.exit()

    print('Done.')


if __name__ == '__main__':
    download()
