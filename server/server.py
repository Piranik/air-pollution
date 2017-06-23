from flask import Flask, jsonify, request, json, Response, send_from_directory
import urllib2
import random
import sys
import re
import os
from flask_cors import CORS, cross_origin
import json
from flask_cache import Cache


from managers.resources_manager import Resources_Manager
from managers.statistics_manager import Statistics_Manager


def _read_romania_data_file():
    ro_data = None
    with open('romania.geojson', 'r') as romania_data_file:
        ro_data = romania_data_file.read()

    return ro_data


if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)
    cache = Cache(app,config={'CACHE_TYPE': 'simple'})

    statistics_manager = Statistics_Manager()
    resources_manager = Resources_Manager()

    @app.route('/api/ro_map_data')
    @cache.cached(timeout=2592000)
    def get_romania_map_data():
        response = {
            'coords': _read_romania_data_file(),
            'center': [45.970, 25.203]
        }

        response = jsonify(response)
        response.status_code = 200

        return response

    @app.route('/api/counties')
    @cache.cached(timeout=2592000)
    def get_counties():
        counties = resources_manager.get_counties()
        response = {
            'counties': counties,
            'counties_number': len(counties)
        }
        response = jsonify(response)
        response.status_code = 200

        return response

    @app.route('/api/statistics/air_pollution_county')
    @cache.cached(timeout=2592000)
    def get_statistics_for_used_stations():
        county_stations_no, statistics = statistics_manager.air_pollution_county_statistics()
        response = {
            'statistics': statistics,
            'number_of_stations': [list(x) for x in county_stations_no]
        }

        response = jsonify(response)
        response.status_code = 200

        return response


    @app.route('/api/viewed_parameters')
    @cache.cached(timeout=2592000)
    def get_parameters():
        viewed_paramters = resources_manager.get_viewed_parameters()
        response = {
            'parameters': viewed_paramters,
            'parameters_len': len(viewed_paramters)
        }
        response = jsonify(response)
        response.status_code = 200

        return response


    @app.route('/api/used_diseases')
    @cache.cached(timeout=2592000)
    def get_used_diseases():
        used_diseases = resources_manager.get_used_diseases()
        used_diseases = [{'_id': x['_id'], 'name': x['name'], 'category': x['category']} for x
                         in used_diseases]
        response = {
            'used_diseases': used_diseases,
            'used_diseases_len': len(used_diseases)
        }
        response = jsonify(response)
        response.status_code = 200

        return response

    @app.route('/api/disease_statistics')
    @cache.cached(timeout=2592000)
    def get_statistics_for_used_diseases():
        statistics, boundaries = statistics_manager.get_disease_county_statistics()
        print len(statistics[0])
        response = {
            'statistics': statistics,
            'boundaries': boundaries
        }

        response = jsonify(response)
        response.status_code = 200

        return response

    @app.route('/api/diseases')
    @cache.cached(timeout=2592000)
    def get_diseases_codification():
        used_diseases = resources_manager.get_used_diseases()
        sorted_used_diseases_names = sorted([disease['name'] for disease in used_diseases])

        used_diseases_indexes = statistics_manager.compute_element_index_codification(
            sorted_used_diseases_names)

        diseases_classification = {}
        for disease in used_diseases:
            if disease['category'] not in diseases_classification:
                diseases_classification[disease['category']] = [disease['name']]
            else:
                diseases_classification[disease['category']].append(disease['name'])

        response = {
            'codification': used_diseases_indexes,
            'diseases_classification': diseases_classification
        }
        response = jsonify(response)
        response.status_code = 200
        return response


    # listen on port 8080 from any host in local network
    app.run(threaded=True, host='0.0.0.0', port='8000', )

