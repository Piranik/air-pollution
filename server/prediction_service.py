from flask import Flask, jsonify, request, json, Response, send_from_directory
from flask_cors import CORS, cross_origin
import json
from flask_cache import Cache
import numpy

from managers.prediction_manager import Prediction_Manager
from managers.resources_manager import Resources_Manager

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)
    cache = Cache(app,config={'CACHE_TYPE': 'simple'})

    prediction_manager = Prediction_Manager()
    resources_manager = Resources_Manager()

    diseases_names = [x['name'] for x in resources_manager.get_used_diseases()]
    prediction_manager.init_prediction_tools()


    @app.route('/api/prediction/info')
    @cache.cached(timeout=2592000)
    def get_prediction_info():
        prediction_tools = prediction_manager.get_prediction_tools_names()
        scores = {}
        for month in xrange(1, 6):
            scores[month] = {}
            for disease_name in diseases_names:
                scores[month][disease_name] = []
                for index in xrange(len(prediction_tools)):
                    scores[month][disease_name].append(prediction_manager.prediction_tools[month][disease_name][index][1])


        response = jsonify({'prediction_tools': prediction_tools, 'scores': scores})
        response.status_code = 200

        return response

    @app.route('/api/prediction/result', methods=['POST'])
    def predict_new_data():
        tool_index = request.json['tool_index']
        disease = request.json['disease']
        months_predicted = request.json['months_predicted']

        predict_data = [
            request.json['aqi_class'],
            request.json['wind_speed_class'],
            request.json['pressure_class'],
            request.json['rainfall_class'],
            request.json['temp_class'],
            request.json['disease_class']
        ]

        predicted_class = prediction_manager.predict(months_predicted, disease, tool_index, predict_data)

        response = jsonify({'prediction_result': predicted_class})
        response.status_code = 200

        return response

    app.run(threaded=True, host='0.0.0.0', port='8003', )
