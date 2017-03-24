from flask import Flask, jsonify, request, json, Response, send_from_directory
import urllib2
import random
import sys
import re
import os
from flask_cors import CORS, cross_origin
import json

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

    statistics_manager = Statistics_Manager()
    resources_manager = Resources_Manager()

    @app.route('/api/ro_map_data')
    def get_romania_map_data():
        response = {
            'coords': _read_romania_data_file(),
            'center': [46.130, 25.203]
        }

        response = jsonify(response)
        response.status_code = 200

        return response

    @app.route('/api/get_counties')
    def get_counties():
        counties = resources_manager.get_counties()
        response = {
            'counties': counties,
            'counties_number': len(counties)
        }


    @app.route('/api/statistics/air_pollution_county')
    def get_statistics_for_used_stations():
        # used_stations_statistics_matrix = resources_manager.get_used_stations_stations()
        county_stations_no, statistics = statistics_manager.air_pollution_county_statistics()
        response = {
            'statistics': statistics,
            'number_of_stations': [list(x) for x in county_stations_no]
        }

        response = jsonify(response)
        response.status_code = 200

        return response


    # listen on port 8080 from any host in local network
    app.run(threaded=True, host='0.0.0.0', port='8000', )

