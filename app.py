from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask_cors import CORS

import json
import copy

app = Flask(__name__)
cors = CORS(app)

data_greece_JHCSSE = None
data_greece_isMOOD_regions = None

def init():
    global data_greece_JHCSSE
    global data_greece_isMOOD_regions

    with open('data/greece/JohnsHopkinsCSSE/timeseries_greece.json') as f:
        data_greece_JHCSSE = json.load(f)['Greece']
    with open('data/greece/isMOOD/regions.json') as regions_file:
    	data_greece_isMOOD_regions = json.load(regions_file)

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

    return jsonify({'regions': data_greece_isMOOD_regions})

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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    init()
    app.run(debug=True)
