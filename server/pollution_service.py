from flask import Flask, jsonify, request, Response, send_from_directory
from flask_cors import CORS, cross_origin
from flask_cache import Cache

from managers.resources_manager import Resources_Manager
from managers.statistics_manager import Statistics_Manager

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)
    cache = Cache(app,config={'CACHE_TYPE': 'simple'})

    statistics_manager = Statistics_Manager()
    resources_manager = Resources_Manager()


    @app.route('/api/pollution/statistics/air_pollution_county')
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


    @app.route('/api/pollution/viewed_parameters')
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


    @app.route('/api/pollution/used_diseases')
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

    app.run(threaded=True, host='0.0.0.0', port='8001', )
