from managers.resources_manager import Resources_Manager
from managers.statistics_manager import Statistics_Manager
from utils import compute_disease_class, compute_input_class

from random import shuffle

from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn import svm

from numpy import mean, array
import pickle
import os.path
import copy
from time import time
import random

_START_YEAR = 2012
_LAST_YEAR = 2017
DISEASE_TRAIN_SET_PERCENTAGE = 0.9
INTERVAL_LENGHT = 6
SCORES_FILENAME = '../pred_scores.pkl'


class Prediction_Manager(object):
    """ Prediction Manager """
    def __init__(self, app_config=None):
        super(Prediction_Manager, self).__init__()
        self.resources_manager = Resources_Manager()
        self.statistics_manager = Statistics_Manager()
        self.load_unchanged_data()
        self.generic_tools = {
            'nn': [
                # 5 x 30
                ('NN 5 x 30 neurons identity', {'solver': 'sgd', 'hidden_layer_sizes': (30, 30, 30, 30, 30), 'activation': 'identity'}),

                ('NN 5 x 30 neurons tanh', {'solver': 'sgd', 'hidden_layer_sizes': (30, 30, 30, 30, 30), 'activation': 'tanh'}),

                ('NN 5 x 30 neurons relu', {'solver': 'sgd', 'hidden_layer_sizes': (30, 30, 30, 30, 30), 'activation': 'relu'}),

                # 3 x 100
                ('NN 3 x 100 neurons identity', {'solver': 'sgd', 'hidden_layer_sizes': (100, 100, 100), 'activation': 'identity'}),

                ('NN 3 x 100 neurons tanh', {'solver': 'sgd', 'hidden_layer_sizes': (100, 100, 100), 'activation': 'tanh'}),

                ('NN 3 x 100 neurons relu', {'solver': 'sgd', 'hidden_layer_sizes': (100, 100, 100), 'activation': 'relu'})
                ],
            'svm': [
                ('SVM poly d1 C-10^-4', {'kernel': 'poly', 'degree': 1, 'C': 0.0001}),
                ('SVM poly d1 C-100', {'kernel': 'poly', 'degree': 1, 'C': 100}),
                ('SVM poly d2', {'kernel': 'poly', 'degree': 2}),
                ('SVM poly d2 coef0-2', {'kernel': 'poly', 'degree': 2, 'coef0': 2}),
                ('SVM poly d3', {'kernel': 'poly', 'degree': 3}),
                ('SVM poly d3 coef0-2', {'kernel': 'poly', 'degree': 3, 'coef0': 2}),

                ('SVM rbf C-10^-5', {'kernel': 'rbf', 'C': 0.00001}),
                ('SVM rbf C-10^-4', {'kernel': 'rbf', 'C': 0.0001}),
                ('SVM rbf C-100', {'kernel': 'rbf', 'C': 100}),
                ('SVM linear', {'kernel': 'linear'})
                ]
        }



    # inputs: AQI_INDEX, Viteza Vant, Presiune Precipitatii, Temparatura, Boala
    # output: disease class {0, 1, 2}
    def load_unchanged_data(self):
        self.sets = []

        self.stations_counties, self.air_pollution = self.statistics_manager.air_pollution_county_statistics()
        self.diseases_statistics, self.boundaries = self.statistics_manager.get_disease_county_statistics()

        counties = [x['name'] for x in self.resources_manager.get_counties()]
        self.counties = sorted(counties)

        parameters = [x['index'] for x in self.resources_manager.get_viewed_parameters()]
        self.parameters = sorted(parameters)

        self.counties_indexes = self.statistics_manager.compute_element_index_codification(
            self.counties)
        self.parameter_indexes = self.statistics_manager.compute_element_index_codification(
            self.parameters)
        self.diseases_indexes = self.statistics_manager.get_diseases_codification()
        self.diseases = map(lambda h: h['name'], self.resources_manager.get_used_diseases())

    def create_datasets(self, disease_name, months_ago):
        datasets = []
        AQI_index = self.parameter_indexes[2000]
        wind_speed_index = self.parameter_indexes[19]
        pressure_index = self.parameter_indexes[22]
        rainfall_index = self.parameter_indexes[24]
        temp_index = self.parameter_indexes[20]
        dox_sulf_index = self.parameter_indexes[1]
        ozone_index = self.parameter_indexes[9]
        pm_aut_index = self.parameter_indexes[4]
        pm_grv_index = self.parameter_indexes[5]
        disease_index = self.diseases_indexes[disease_name]
        last_disease = None
        for county in self.counties:
            countyIndex = self.counties_indexes[county]
            # last_disease = None
            if self.stations_counties[countyIndex]:
                for year in xrange(2, _LAST_YEAR - _START_YEAR):
                    for month in xrange(0, 12):
                        new_month = month - months_ago
                        new_year = year
                        if new_month < 0:
                            new_year -= 1
                            new_month += 12

                        disease_value = (
                            self.diseases_statistics[countyIndex][year][month][disease_index])
                        last_disease_value = (
                                self.diseases_statistics[countyIndex][new_year][new_month][disease_index])
                        if disease_value > 0 and last_disease_value > 0:

                            disease_class = compute_disease_class(
                                self.boundaries[disease_index],
                                disease_value)

                            last_disease_class = compute_disease_class(
                                self.boundaries[disease_index],
                                last_disease_value)

                            # compute average of 6 months
                            AQI_avg = []
                            wind_speed_avg = []
                            pressure_avg = []
                            rainfall_avg = []
                            temp_avg = []
                            while (new_year == year and new_month <= month) or new_year < year:
                                AQI_value = (
                                    self.air_pollution[countyIndex][new_year][new_month][AQI_index])
                                AQI_avg.append(AQI_value)

                                wind_speed_value = (
                                    self.air_pollution[countyIndex][new_year][new_month][wind_speed_index])
                                if wind_speed_value != 0:
                                    wind_speed_avg.append(wind_speed_value)
                                pressure_value = (
                                    self.air_pollution[countyIndex][new_year][new_month][pressure_index])
                                if pressure_value != 0:
                                    pressure_avg.append(pressure_value)

                                rainfall_value = (
                                    self.air_pollution[countyIndex][new_year][new_month][rainfall_index])
                                if rainfall_value != 0:
                                    rainfall_avg.append(rainfall_value)
                                temp_value = (
                                    self.air_pollution[countyIndex][year][month][temp_index])
                                if temp_value != 0:
                                    temp_avg.append(temp_value)

                                new_month += 1
                                if new_month > 11:
                                    new_month %= 12
                                    new_year += 1

                                # print AQI_avg, monoxid_avg, wind_speed_avg, pressure_avg,
                                # rainfall_avg, temp_avg
                                # experiment cu clase in loc de valori pt X luni

                            aqi_class = mean(AQI_avg)

                            if wind_speed_avg:
                                wind_speed_class = compute_input_class(
                                    19,
                                    mean(wind_speed_avg))
                            else:
                                wind_speed_class = 0

                            if pressure_avg:
                                pressure_class = compute_input_class(
                                    22,
                                    mean(pressure_avg))
                            else:
                                pressure_class = 0

                            if rainfall_avg:
                                rainfall_class = compute_input_class(
                                    24,
                                    mean(rainfall_avg), month)
                            else:
                                rainfall_class = 0

                            if temp_avg:
                                temp_class = compute_input_class(20, mean(temp_avg), month)
                            else:
                                temp_class = 0

                            datasets.append(
                                ([aqi_class, wind_speed_class, pressure_class,
                                  rainfall_class, temp_class, last_disease_class],
                                 disease_class))
        return datasets

    def create_train_test_from_datasets(self, datasets):
        shuffle(datasets)
        train_input = []
        train_output = []
        test_input = []
        test_output = []
        test_classes_counter = [0] * 3
        train_classes_counter = [0] * 3
        train_set_len = int(len(datasets) * DISEASE_TRAIN_SET_PERCENTAGE)
        print len(datasets)
        for index in xrange(train_set_len):
            train_input.append(datasets[index][0])
            train_output.append(datasets[index][1])
            train_classes_counter[datasets[index][1]] += 1
        for index in xrange(train_set_len, len(datasets)):
            test_input.append(datasets[index][0])
            test_output.append(datasets[index][1])
            test_classes_counter[datasets[index][1]] += 1
        return datasets[:train_set_len], test_input, test_output, train_classes_counter, test_classes_counter

    def predict_nn(self, train_x, train_t, test_x, test_t):
        # print train_x
        scaler = StandardScaler()
        scaler.fit(train_x)
        # train_x = scaler.transform(train_x)
        # test_x = scaler.transform(test_x)
        nn = MLPClassifier(hidden_layer_sizes=(100, 100, 100))
        nn.fit(train_x, train_t)
        return nn.score(test_x, test_t)

    def predict_svm(self, train_x, train_t, test_x, test_t):
        clf = svm.SVC(decision_function_shape='ovo', **{'kernel': 'poly', 'degree': 2})
        clf.fit(train_x, train_t)
        return clf.score(test_x, test_t)

    def init_prediction_tools(self):
        prediction_tools = {}

        # load conf
        if os.path.isfile(SCORES_FILENAME):
            with open(SCORES_FILENAME, 'rb') as scores_file:
                prediction_tools = pickle.load(scores_file)
        else:
            # generate new prediction tools
            for month in xrange(1, INTERVAL_LENGHT):
                prediction_tools[month] = {}
                for disease in self.diseases:
                    prediction_tools[month][disease] = []
                    # NN params
                    dataset = self.create_datasets(disease, month)
                    for nn_params in self.generic_tools['nn']:
                        max_nn = None
                        max_score = 0.0
                        time_total = 0.0
                        for _ in xrange(10):
                            train_set, test_x, test_t, _, _ = self.create_train_test_from_datasets(dataset)
                            new_nn = MLPClassifier(warm_start=True, **nn_params[1])
                            train_x = []
                            train_t = []
                            shuffle(train_set)
                            for index in xrange(len(train_set)):
                                train_x.append(train_set[index][0])
                                train_t.append(train_set[index][1])
                            t0 = time()
                            new_nn.fit(train_x, train_t)
                            time_total += time() - t0
                            new_score = new_nn.score(test_x, test_t)
                            print month, disease, nn_params[0], new_score
                            if new_score > max_score:
                                max_score = new_score
                                max_nn = copy.deepcopy(new_nn)
                        print 'Saving %f in time %f' % (max_score, time_total/10)
                        prediction_tools[month][disease].append((max_nn, max_score, time_total/10))


                    for svm_params in self.generic_tools['svm']:
                        max_svm = None
                        max_score = 0.0
                        time_total = 0.0
                        for index in xrange(10):
                            train_set, test_x, test_t, _, _ = self.create_train_test_from_datasets(dataset)
                            new_svm = svm.SVC(decision_function_shape='ovo', cache_size=2, **svm_params[1])

                            train_x = []
                            train_t = []
                            shuffle(train_set)
                            for index in xrange(len(train_set)):
                                train_x.append(train_set[index][0])
                                train_t.append(train_set[index][1])
                            t0 = time()
                            new_svm.fit(train_x, train_t)
                            time_total += time() - t0
                            new_score = new_svm.score(test_x, test_t)
                            if new_score > max_score:
                                max_score = new_score
                                max_svm = copy.deepcopy(new_svm)
                            print month, disease, svm_params[0], new_score
                        print 'Saving %f in time %f' % (max_score, time_total/10)
                        prediction_tools[month][disease].append((max_svm, max_score, time_total/10))
            # save conf
            with open(SCORES_FILENAME, 'wb') as scores_file:
                pickle.dump(prediction_tools, scores_file, pickle.HIGHEST_PROTOCOL)

        self.prediction_tools = prediction_tools


    def get_prediction_tools_names(self):
        index = 0
        tools = {}
        for tool in self.generic_tools['nn']:
            tools[tool[0]] = index
            index += 1

        for tool in self.generic_tools['svm']:
            tools[tool[0]] = index
            index += 1
        return tools


    def init_pred_tools_mock(self):
        prediction_tools = {}
        for month in xrange(1, INTERVAL_LENGHT):
            prediction_tools[month] = {}
            for disease in self.diseases:
                prediction_tools[month][disease] = []
                # NN params
                for nn_params in self.generic_tools['nn']:
                    prediction_tools[month][disease].append((None, random.random(), 5*random.random()))
                for svm_params in self.generic_tools['svm']:
                    prediction_tools[month][disease].append((None, random.random(), 5*random.random()))
        self.prediction_tools_mock = prediction_tools

    def predict(self, month, disease, tool_index, predict_data):
        tool = self.prediction_tools[month][disease][tool_index][0]
        predict_data = array(predict_data).reshape(1, -1)
        predction_result = tool.predict(predict_data)[0]
        print predction_result
        return predction_result


if __name__ == '__main__':
    pm = Prediction_Manager()
    print "Boala\tLungime set antrenare\tScore NN"
    pm.init_prediction_tools()
    tool_names = pm.get_prediction_tools_names()
    x = len(pm.generic_tools['nn'])
    for m in pm.prediction_tools.keys():
        for d in pm.prediction_tools[m].keys():
            for l in xrange(x, len(pm.prediction_tools[m][d])):
                pm.prediction_tools[m][d][l] = (
                    pm.prediction_tools[m][d][l][1],
                    pm.prediction_tools[m][d][l][0],
                    pm.prediction_tools[m][d][l][2])
    with open(SCORES_FILENAME, 'wb') as scores_file:
        pickle.dump(pm.prediction_tools, scores_file, pickle.HIGHEST_PROTOCOL)

