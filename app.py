from flask import Flask, jsonify, abort, make_response, send_from_directory, render_template
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

import json
import copy
import pandas as pd
import datetime

app = Flask(__name__)
cors = CORS(app)

data_greece_JHCSSE = None
data_greece_isMOOD_regions = None
data_greece_isMOOD_total_info = None
data_greece_isMOOD_cases_region_timeline = None
data_greece_wikipedia = None
population_per_region = None 

def init():
    global data_greece_JHCSSE
    global data_greece_isMOOD_regions
    global data_greece_isMOOD_total_info
    global data_greece_isMOOD_cases_region_timeline
    global data_greece_wikipedia
    global population_per_region


    with open('data/greece/JohnsHopkinsCSSE/timeseries_greece.json') as f:
        data_greece_JHCSSE = json.load(f)['Greece']
    with open('data/greece/isMOOD/regions.json') as regions_file:
    	data_greece_isMOOD_regions = json.load(regions_file)
    with open('data/greece/isMOOD/total-info.json') as f:
    	data_greece_isMOOD_total_info = json.load(f)
    with open('data/greece/isMOOD/cases_by_region_timeline.csv', encoding = 'utf-8') as f:
    	data_greece_isMOOD_cases_region_timeline = pd.read_csv(f)
    data_greece_isMOOD_cases_region_timeline = data_greece_isMOOD_cases_region_timeline.where(pd.notnull(data_greece_isMOOD_cases_region_timeline), None)

    with open('data/greece/wikipedia/cases.csv', encoding = 'utf-8') as cases_file:
    	data_greece_wikipedia = pd.read_csv(cases_file)
    data_greece_wikipedia = data_greece_wikipedia.where(pd.notnull(data_greece_wikipedia), None)

    with open('data/greece/isMOOD/population_per_region.json') as f:
        population_per_region = json.load(f)

init()

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
        date['active'] = date['confirmed'] - date['deaths'] - date['recovered']

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
                region['cases_per_100000_people'] = round(region['region_cases'] / region['population'] * 100000.0, 2)

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


    return jsonify({'cases': out_json})


@app.route('/total', methods=['GET'])
def get_total():
    out_json = copy.deepcopy(data_greece_JHCSSE[-1])
    out_json['active'] = out_json['confirmed'] - out_json['deaths'] - out_json['recovered']

    return jsonify({'cases': out_json})


@app.route('/total-tests', methods=['GET'])
def get_total_tests():

    date = list(data_greece_wikipedia['Date'])[:-1]
    total_tests = list(data_greece_wikipedia['Cumulative tests performed'])[:-1]
    total_tests = [int(i) if i!=None else None for i in total_tests]
    out_json = [{'date': date, 'tests':tests} for date, tests in zip(date, total_tests)]

    return jsonify({'total_tests': out_json})

@app.route('/intensive-care', methods=['GET'])
def get_intensive_care():

    date = list(data_greece_wikipedia['Date'])[:-1]
    intensive_care = list(data_greece_wikipedia['In intensive care (total)'])[:-1]
    intensive_care = [int(i) if i!=None else None for i in intensive_care]
    out_json = [{'date': date, 'intensive_care':num_patients} for date, num_patients in zip(date, intensive_care)]

    return jsonify({'cases': out_json})

@app.route('/gender-distribution', methods=['GET'])
def get_genders():

    out_json = {
        'total_females': data_greece_isMOOD_total_info[0]['total_females'] / 10.0,
        'total_males': data_greece_isMOOD_total_info[0]['total_males'] / 10.0
    }

    return jsonify({'gender_percentages': out_json})

@app.route('/age-distribution', methods=['GET'])
def get_age_groups():

    out_json = {
        'age_average': data_greece_isMOOD_total_info[0]['age_average'],
        'average_death_age': data_greece_isMOOD_total_info[0]['average_death_age'],
        'total_age_groups': data_greece_isMOOD_total_info[0]['total_age_groups']
    }

    return jsonify({'age_distribution': out_json})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()
