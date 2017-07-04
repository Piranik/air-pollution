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
import xlsxwriter
from heapq import heappop, heappush

import pylab


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


    def create_statistics_NN(self):
        XLS_NAME = 'NN_table.xlsx'
        diseases = self.resources_manager.get_used_diseases()
        workbook = xlsxwriter.Workbook(XLS_NAME)
        worksheet = workbook.add_worksheet()

        format = workbook.add_format()
        format.set_bg_color('#FFE599')

        row = 0
        # Headers
        worksheet.write(0, 0, 'Denumire Boala')
        worksheet.write(0, 1, 'Luni folosite')
        for index in xrange(len(self.generic_tools['nn'])):
            worksheet.write(0, 2 + index, self.generic_tools['nn'][index][0])
        row += 1
        # Content
        for disease in diseases:
            worksheet.write(row, 0, disease['name'])
            for month in xrange(1, 6):
                worksheet.write(row, 1, month)
                my_max = 0
                cols_max = []
                for index in xrange(len(self.generic_tools['nn'])):
                    value = round(self.prediction_tools[month][disease['name']][index][1] * 100, 2)
                    if value > my_max:
                        my_max = value
                        cols_max = [index]
                    elif value == my_max:
                        cols_max.append(index)
                    worksheet.write(row, 2+index, value)
                for index in cols_max:
                    worksheet.write(row, 2+index, my_max, format)

                row += 1
        workbook.close()

    def create_statistics_SVM(self):
        XLS_NAME = 'SVM_table.xlsx'
        step = len(self.generic_tools['nn'])
        diseases = self.resources_manager.get_used_diseases()
        workbook = xlsxwriter.Workbook(XLS_NAME)
        worksheet = workbook.add_worksheet()

        format = workbook.add_format()
        format.set_bg_color('#FFE599')

        row = 0
        # Headers
        worksheet.write(0, 0, 'Denumire Boala')
        worksheet.write(0, 1, 'Luni folosite')
        for index in xrange(len(self.generic_tools['svm'])):
            worksheet.write(0, 2 + index, self.generic_tools['svm'][index][0])
        row += 1
        # Content
        for disease in diseases:
            worksheet.write(row, 0, disease['name'])
            for month in xrange(1, 6):
                worksheet.write(row, 1, month)
                my_max = 0
                cols_max = []
                for index in xrange(len(self.generic_tools['svm'])):
                    value = round(self.prediction_tools[month][disease['name']][step + index][1] * 100, 2)
                    if value > my_max:
                        my_max = value
                        cols_max = [index]
                    elif value == my_max:
                        cols_max.append(index)
                    worksheet.write(row, 2+index, value)
                for index in cols_max:
                    worksheet.write(row, 2+index, my_max, format)

                row += 1
        workbook.close()

    def best_NN(self):
        XLS_NAME = 'NN_best.xlsx'
        diseases = self.resources_manager.get_used_diseases()
        workbook = xlsxwriter.Workbook(XLS_NAME)
        worksheet = workbook.add_worksheet()

        format = workbook.add_format()
        format.set_bg_color('#FFE599')


        # Content
        heapq = []
        for disease in diseases:

            # worksheet.write(row, 0, disease['name'])
            for month in xrange(1, 6):
                # worksheet.write(row, 1, month)
                line = [disease['name'], month]
                my_max = 0
                cols_max = []
                for index in xrange(len(self.generic_tools['nn'])):
                    value = round(self.prediction_tools[month][disease['name']][index][1] * 100, 2)
                    line.append(value)
                    if value > my_max:
                        my_max = value
                        cols_max = [index]
                    elif value == my_max:
                        cols_max.append(index)
                    # worksheet.write(row, 2+index, value)
                # for index in cols_max:
                #     worksheet.write(row, 2+index, my_max, format)
                # row += 1
                heappush(heapq, (-1 * my_max, cols_max, line))

        row = 0
        # Headers
        worksheet.write(0, 0, 'Denumire Boala')
        worksheet.write(0, 1, 'Luni folosite')
        for index in xrange(len(self.generic_tools['nn'])):
            worksheet.write(0, 2 + index, self.generic_tools['nn'][index][0])
        row += 1

        for i in xrange(15):
            line = heappop(heapq)
            for index, value in enumerate(line[2]):
                if index-2 in line[1]:
                    worksheet.write(row, index, value, format)
                else:
                    worksheet.write(row, index, value)
            row += 1


        workbook.close()


    def best_SVM(self):
        XLS_NAME = 'SVM_best.xlsx'
        diseases = self.resources_manager.get_used_diseases()
        workbook = xlsxwriter.Workbook(XLS_NAME)
        worksheet = workbook.add_worksheet()

        step = len(self.generic_tools['nn'])

        format = workbook.add_format()
        format.set_bg_color('#FFE599')


        # Content
        heapq = []
        for disease in diseases:

            # worksheet.write(row, 0, disease['name'])
            for month in xrange(1, 6):
                # worksheet.write(row, 1, month)
                line = [disease['name'], month]
                my_max = 0
                cols_max = []
                for index in xrange(len(self.generic_tools['svm'])):
                    value = round(self.prediction_tools[month][disease['name']][step + index][1] * 100, 2)
                    line.append(value)
                    if value > my_max:
                        my_max = value
                        cols_max = [index]
                    elif value == my_max:
                        cols_max.append(index)
                    # worksheet.write(row, 2+index, value)
                # for index in cols_max:
                #     worksheet.write(row, 2+index, my_max, format)
                # row += 1
                heappush(heapq, (-1 * my_max, cols_max, line))

        row = 0
        # Headers
        worksheet.write(0, 0, 'Denumire Boala')
        worksheet.write(0, 1, 'Luni folosite')
        for index in xrange(len(self.generic_tools['svm'])):
            worksheet.write(0, 2 + index, self.generic_tools['svm'][index][0])
        row += 1

        for i in xrange(15):
            line = heappop(heapq)
            for index, value in enumerate(line[2]):
                if index-2 in line[1]:
                    worksheet.write(row, index, value, format)
                else:
                    worksheet.write(row, index, value)
            row += 1

        workbook.close()



    def sigmoid_effects(self):
        conf = {
            'Boala interstitiala pulmonara': [1],
            'Accident vascular cerebral': [1, 2, 3, 4],
            'Neoplasm pulmonar': [2],
            'Tulburari vasculare': [4, 3]
        }

        tools = [
            {'solver': 'sgd', 'hidden_layer_sizes': (30, 30, 30, 30, 30), 'activation': 'logistic'},
            {'solver': 'sgd', 'hidden_layer_sizes': (100, 100, 100), 'activation': 'logistic'},
            {'kernel': 'sigmoid'}
        ]

        # headers
        XLS_NAME = 'Sigmoid_table.xlsx'
        workbook = xlsxwriter.Workbook(XLS_NAME)
        worksheet = workbook.add_worksheet()

        # format = workbook.add_format()
        # format.set_bg_color('#FFE599')

        # Headers
        worksheet.write(0, 0, 'Denumire Boala')
        worksheet.write(0, 1, 'Luni folosite')
        worksheet.write(0, 2, 'F1')
        worksheet.write(0, 3, 'F2')
        worksheet.write(0, 4, 'F3')

        row = 1
        for disease in conf:
            worksheet.write(row, 0, disease)
            for month in conf[disease]:
                worksheet.write(row, 1, month)
                dataset = self.create_datasets(disease, month)
                train_set, test_x, test_t, _, _ = self.create_train_test_from_datasets(dataset)
                train_x = []
                train_t = []
                shuffle(train_set)
                for index in xrange(len(train_set)):
                    train_x.append(train_set[index][0])
                    train_t.append(train_set[index][1])
                model = MLPClassifier(**tools[0])
                model.fit(train_x, train_t)
                score = model.score(test_x, test_t)
                worksheet.write(row, 2, round(score * 100, 2))

                model = MLPClassifier(**tools[1])
                model.fit(train_x, train_t)
                score = model.score(test_x, test_t)
                worksheet.write(row, 3, round(score * 100, 2))

                model = svm.SVC(**tools[2])
                model.fit(train_x, train_t)
                score = model.score(test_x, test_t)
                worksheet.write(row, 4, round(score * 100, 2))
                row += 1
        workbook.close()



    def create_plots_SVM(self):
        pylab.axis([0, 6, 0, 1])

        # Cost1 vs cost2 plot
        disease = 'Accident vascular cerebral'
        x = [1, 2, 3, 4, 5]
        c1 = []
        c2 = []
        for i in x:
            c1.append(self.prediction_tools[i][disease][12][2])
            c2.append(self.prediction_tools[i][disease][14][2])

        pylab.plot(x,c1, label='Cost 0.0001')
        pylab.plot(x,c2, label='Cost 100')

        pylab.legend(loc='upper right')
        pylab.xlabel('Luna')
        pylab.ylabel('Timp de antrenare (s)')

        pylab.show()

        # # D2 vs D3 plot
        # disease = 'Accident vascular cerebral'
        # x = [1, 2, 3, 4, 5]
        # d2 = []
        # d3 = []
        # for i in x:
        #     d2.append(self.prediction_tools[i][disease][8][2])
        #     d3.append(self.prediction_tools[i][disease][10][2])

        # pylab.plot(x,d2, label='Gradul 2')
        # pylab.plot(x,d3, label='Gradul 3')

        # pylab.legend(loc='upper right')
        # pylab.xlabel('Luna')
        # pylab.ylabel('Timp de antrenare (s)')

        # pylab.show()

        # # NN 1 vs NN2
        # disease = 'Accident vascular cerebral'

        # x = [1, 2, 3, 4, 5]
        # n1 = [0.0] * 5
        # n2 = [0.0] * 5
        # diseases = self.resources_manager.get_used_diseases()
        # for i in x:
        #     for disease in diseases:
        #         n1[i-1] += self.prediction_tools[i][disease['name']][0][2]
        #         n2[i-1] += self.prediction_tools[i][disease['name']][3][2]

        # for i in x:
        #     n1[i-1] /= len(diseases)
        #     n2[i-1] /= len(diseases)

        # pylab.plot(x,n1, label='NN 5 x 30')
        # pylab.plot(x,n2, label='NN 3 x 100')

        # pylab.legend(loc='upper right')
        # pylab.xlabel('Luna')
        # pylab.ylabel('Timp de antrenare (s)')

        # pylab.show()


if __name__ == '__main__':
    pm = Prediction_Manager()
    # print "Boala\tLungime set antrenare\tScore NN"
    pm.init_prediction_tools()
    # pm.create_statistics_NN()
    # pm.create_statistics_SVM()
    # pm.best_NN()
    # pm.best_SVM()
    pm.create_plots_SVM()
    # pm.sigmoid_effects()
