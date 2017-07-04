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

    @app.route('/api/diseases/disease_statistics')
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

    @app.route('/api/diseases/list')
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

    # @app.route('/api/pollution/used_diseases')
    # @cache.cached(timeout=2592000)
    # def get_used_diseases():
    #     used_diseases = resources_manager.get_used_diseases()
    #     used_diseases = [{'_id': x['_id'], 'name': x['name'], 'category': x['category']} for x
    #                      in used_diseases]
    #     response = {
    #         'used_diseases': used_diseases,
    #         'used_diseases_len': len(used_diseases)
    #     }
    #     response = jsonify(response)
    #     response.status_code = 200

    #     return response

    app.run(threaded=True, host='0.0.0.0', port='8002', )
