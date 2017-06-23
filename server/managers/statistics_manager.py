from config_utils.config import ConfigYaml
from managers.resources_manager import Resources_Manager
from datetime import datetime
import re

AQI_INDEXES = {
    1: [50, 74, 124, 349, 499],
    5: [10, 20, 30, 40, 100],
    9: [40, 80, 120, 180, 240],
    1001: [50, 100, 140, 200, 400]
}

CANONIC_COUNTY_NAMES = {
    'dimbovita': 'dambovita',
    'vilcea': 'valcea'
}

DISEASE_CONFIGURATION = {
    'Neoplasm' : {
        'Neoplasm pulmonar': ['E3122', 'E3121', 'E3123'],
        'Neoplasm renal': ['L3031', 'L3032'],
        'Neoplasm al sistemului nervos': ['B3071']
    },

    'Afectiuni Neurologice': {
        'Accident vascular cerebral': ['B3113', 'B3112', 'B3114', 'F3142', 'F3141']
    },

    'Afectiuni Cardiovasculare': {
        'Hipertensiune': ['F3081', 'F3082'],
        'Artmie': ['F3111', 'F3121', 'F3122', 'F3112'],
        'Tulburari vasculare': ['F3041', 'F3042', 'F3071', 'F3062', 'F3061', 'F2031', 'F3011',
                                'F3012', 'F2021', 'F3013'],
        'Insuficienta Cardiaca': ['F3032', 'F3031', 'F3101', 'F3161'],
        'Angina': ['F3131', 'F3132']
    },

    'Afectiuni Respiratorii': {
        'Astm': ['E3102', 'E3101', 'E3103'],
        'Infectii respiratorii': ['E3031', 'E3032', 'E3033', 'E3081', 'D3050', 'E3111', 'E3112'],
        'BPOC': ['E3061', 'E3062'],
        'Boala interstitiala pulmonara': ['E3151', 'E3152', 'E3153'],
        'Edem pulmonar': ['E3050']
    },

    'Afectiuni dermatologice': {
        'Tulburari ale pielii': ['J3071', 'J3061', 'J3052']
    },

    'Afectiuni hematologice': {
        'Leucemie': ['R3022', 'R3012', 'R3011', 'R3013'],
        'Tulburari ale globulelor rosii': ['Q3023', 'Q3022', 'Q3021'],
        'Anomalii de coagulare': ['Q3030']
    },

    'Afectiuni Oftalmologice': {
        'Infecti oculare': ['C3011', 'C3012'],
        'Leziuni oculare': ['C1010', 'C1070', 'C1080', 'C3030'],
        'Tulburari oculare': ['C3042', 'C3041', 'C1100', 'C1111', 'C3020', 'C1020']
    },

    'Afectiuni imunologice': {
        'Tulburari reticuloendoteliale': ['Q3011', 'Q3013'],
        'Reactii alergice': ['X3020']
    },

    'Afectiuni Metabolice': {
        'Tulburari metabolice': ['K3031', 'K3033']
    }
}


DISEASE_BOUNDARIES = {
    'Neoplasm pulmonar' : [0.22, 0.32],
    'Neoplasm renal' : [0.11, 0.17],
    'Neoplasm al sistemului nervos' : [0.07, 0.12],
    'Accident vascular cerebral' : [0.3, 0.45],
    'Hipertensiune' : [0.22, 0.375],
    'Artmie' : [0.14, 0.24],
    'Tulburari vasculare' : [0.26, 0.39],
    'Insuficienta Cardiaca' : [0.38, 0.55],
    'Angina' : [0.09, 0.16],
    'Astm' : [0.16, 0.27],
    'Infectii respiratorii' : [0.37, 0.55],
    'BPOC' : [0.3, 0.45],
    'Boala interstitiala pulmonara' : [0.19, 0.39],
    'Edem pulmonar' : [0.16, 0.295],
    'Tulburari ale pielii' : [0.215, 0.305],
    'Leucemie' : [0.17, 0.26],
    'Tulburari ale globulelor rosii' : [0.115, 0.17],
    'Anomalii de coagulare' : [0.07, 0.105],
    'Infecti oculare' : [0.05, 0.12],
    'Leziuni oculare' : [0.097, 0.15],
    'Tulburari oculare' : [0.24, 0.34],
    'Tulburari reticuloendoteliale' : [0.065, 0.14],
    'Reactii alergice': [0.07, 0.10],
    'Tulburari metabolice': [0.06, 0.115]
}

# DISEASE_BOUNDARIES = [0.1, 0.2, 0.3, 0.4, 0.6]
# DISEASE_BOUNDARIES = [0.15, 0.5]

NO2_INDEX = 1001
NOx_INDEX = 3
NO_INDEX = 10
RAINFALL_INDEX = 24
AQI_INDEX = 2000
MONTHS = ['01', '02', '03', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
_START_YEAR = 2010
_LAST_YEAR = 2017


def compute_average(measurements):
    if measurements:
        measurements_sum = 0
        for measurement in measurements:
            measurements_sum += float(measurement['value'])

        return float(measurements_sum) / len(measurements)
    return 0


def compute_sum(measurements):
    if measurements:
        measurements_sum = 0.0
        for measurement in measurements:
            measurements_sum += float(measurement['value'])
        return measurements_sum
    return 0


class Statistics_Manager(object):
    """Statistics Manager for Stations"""

    def __init__(self):
        super(Statistics_Manager, self).__init__()
        self.resources_manager = Resources_Manager()
        self.counties = self.resources_manager.get_counties()

    @staticmethod
    def compute_air_quality_index(params_codif, params_values):
        max_index = -1
        for param_indentifier in AQI_INDEXES:
            index = 0
            param_value = params_values[params_codif[param_indentifier]]
            if param_value <= 0:
                continue
            for val in AQI_INDEXES[param_indentifier]:
                if param_value < val:
                    break
                index += 1
            max_index = max(max_index, index)
        return max_index + 1

    @staticmethod
    def compute_element_index_codification(elements):
        elements_indexes = {}
        index = 0
        for element in elements:
            elements_indexes[element] = index
            index += 1
        return elements_indexes

    """
    This function must not be here.
    It will be placed in statistics_manager.
    """
    def compute_statistics_for_station(self, station, parameters, resources_manager):
        station_statistics = {}
        station_statistics['internationalCode'] = station['internationalCode']
        station_statistics['county'] = station['county']
        statistics = []
        for year in xrange(_START_YEAR, _LAST_YEAR):
            for month in MONTHS:
                parameter_value_dict = {}
                for parameter in parameters:
                    if parameter['index'] == NO2_INDEX:
                        measurements_NOx = resources_manager.get_measurements_for_station(
                            station['internationalCode'], year, month, NOx_INDEX)
                        measurements_NO = resources_manager.get_measurements_for_station(
                            station['internationalCode'], year, month, NO_INDEX)

                        if measurements_NO and measurements_NOx:
                            NOx_avg = compute_average(measurements_NOx[0]['measurements'])
                            NO_avg = compute_average(measurements_NO[0]['measurements'])
                            NO2_avg = NOx_avg - NO_avg
                            if NO2_avg > 0 and NOx_avg > 0 and NO_avg > 0:
                                parameter_value_dict[str(NO2_INDEX)] = NO2_avg
                            else:
                                parameter_value_dict[str(NO2_INDEX)] = 0

                        else:
                            parameter_value_dict[str(NO2_INDEX)] = 0
                    else:
                        measurements = resources_manager.get_measurements_for_station(
                            station['internationalCode'], year, month, parameter['index'])
                        if measurements:
                            if parameter['index'] == RAINFALL_INDEX:
                                parameter_value_dict[str(parameter['index'])] = compute_sum(
                                    measurements[0]['measurements'])
                            else:
                                parameter_value_dict[str(parameter['index'])] = compute_average(
                                    measurements[0]['measurements'])
                        else:
                            parameter_value_dict[str(parameter['index'])] = 0
                statistics.append({'year': year, 'month': month, 'values': parameter_value_dict})

        station_statistics['statistics'] = statistics
        return station_statistics

    def create_statistics_for_diseases(self):
        counties = self.resources_manager.get_counties()

        for disease_category in DISEASE_CONFIGURATION:
            for disease_name in DISEASE_CONFIGURATION[disease_category]:
                initial_disease_statistics = []
                used_disease_object = {}
                used_disease_object['name'] = disease_name
                used_disease_object['category'] = disease_category
                used_disease_object['avg_cases'] = 0.0
                statistics = {}

                for disease_code in DISEASE_CONFIGURATION[disease_category][disease_name]:
                    disease = self.resources_manager.get_disease_by_code(disease_code)
                    initial_disease_statistics.append(disease)

                for county in counties:
                    county_statistic_obj = {}
                    for year in xrange(_START_YEAR, _LAST_YEAR):
                        county_statistic_obj[str(year)] = {}
                        for month in range(12):
                            county_statistic_obj[str(year)][str(month)] = 0
                    statistics[county['name']] = county_statistic_obj

                for disease in initial_disease_statistics:
                    used_disease_object['avg_cases'] += disease['avg_cases']
                    for statistic in disease['statistics']:
                        date = datetime.strptime(statistic['start_date'], '%d.%m.%Y')
                        statistic_county = (CANONIC_COUNTY_NAMES[statistic['county']]
                                            if statistic['county'] in CANONIC_COUNTY_NAMES
                                            else statistic['county'])
                        statistic_year = date.strftime('%Y')
                        statistic_month = str(int(date.strftime('%m'))-1)
                        statistics[statistic_county][statistic_year][statistic_month] += (
                            statistic['total_number_cases'])
                used_disease_object['statistics'] = statistics
                self.resources_manager.insert_update_disease_statistics(used_disease_object)


    def air_pollution_county_statistics(self):
        """Return statistics between air_pollution and counties.

        Returns:
            statistics: 4-dimensional matrix. stastics[county][year][month][parameter] = value

        """

        counties = [x['name'] for x in self.resources_manager.get_counties()]
        counties = sorted(counties)

        parameters = [x['index'] for x in self.resources_manager.get_viewed_parameters()]
        parameters = sorted(parameters)
        # remove AQI
        parameters.remove(AQI_INDEX)

        counties_indexes = self.compute_element_index_codification(counties)
        parameter_indexes = self.compute_element_index_codification(parameters)

        stations_statistics = self.resources_manager.get_stations_statistics()

        statistics = [[[[0 for _ in parameters] for _ in range(12)] for _ in range(2010, 2017)]
                      for _ in counties]
        statistics_stations = [[[[0 for _ in parameters] for _ in range(12)] for _ in range(2010, 2017)]
                      for _ in counties]

        stations_in_counties = [set() for county in counties]

        print parameter_indexes
        print parameters

        # Create 4d matrix of statistics for each county
        for station in stations_statistics:
            county_index = counties_indexes[station['county']]
            stations_in_counties[county_index].add(station['internationalCode'])
            for statistic in station['statistics']:
                statistic_year = int(statistic['year'])
                if statistic_year >= _START_YEAR:
                    year_index = statistic_year - _START_YEAR
                    month = int(statistic['month']) - 1
                    for parameter in statistic['values']:
                        if int(parameter) in parameter_indexes:
                            parameter_index = parameter_indexes[int(parameter)]
                            statistics[county_index][year_index][month][parameter_index] += (
                                statistic['values'][parameter])
                            if statistic['values'][parameter] > 0:
                                statistics_stations[county_index][year_index][month][parameter_index] += 1

        for county in counties:
            county_index = counties_indexes[county]
            for year_index in range(_LAST_YEAR - _START_YEAR):
                for month_index in range(12):
                    for param_index in range(len(parameters)-1):
                        stations_no = (
                            statistics_stations[county_index][year_index][month][parameter_index])
                        if stations_no > 0:
                            statistics[county_index][year_index][month_index][param_index] /= (
                                stations_no)
                    aqi_index = self.compute_air_quality_index(
                        parameter_indexes,
                        statistics[county_index][year_index][month_index])
                    statistics[county_index][year_index][month_index].append(aqi_index)


        return stations_in_counties, statistics

    def get_disease_county_statistics(self):
        """Return statistics between diseases and counties.

        Returns:
            statistics: 4-dimensional matrix. stastics[county][year][month][disease] = value
        """
        counties = [x['name'] for x in self.resources_manager.get_counties()]
        counties = sorted(counties)
        counties_indexes = self.compute_element_index_codification(counties)

        used_diseases = self.resources_manager.get_used_diseases()
        sorted_used_diseases_names = sorted([disease['name'] for disease in used_diseases])
        used_diseases_indexes = self.compute_element_index_codification(sorted_used_diseases_names)
        statistics = [[[[0 for _ in used_diseases] for _ in range(12)] for _ in
                       range(_START_YEAR, _LAST_YEAR)] for _ in counties]

        for disease in used_diseases:
            disease_index = used_diseases_indexes[disease['name']]
            for county in disease['statistics']:
                county_index = counties_indexes[county]
                for year in disease['statistics'][county]:
                    statistic_year = int(year)
                    if statistic_year >= _START_YEAR:
                        year_index = statistic_year - _START_YEAR
                        for month in disease['statistics'][county][year]:
                            month_index = int(month)
                            statistics[county_index][year_index][month_index][disease_index] = (
                                disease['statistics'][county][year][month])

        diseases_boundaries = {}
        for disease in used_diseases:
            disease_index = used_diseases_indexes[disease['name']]
            disease_values = set()
            for county in disease['statistics']:
                for year in disease['statistics'][county]:
                    if statistic_year >= _START_YEAR:
                        for month in disease['statistics'][county][year]:
                            disease_values.add(disease['statistics'][county][year][month])
            disease_values = sorted(disease_values)
            disease_values_len = len(disease_values)
            diseases_boundaries[disease_index] = [int(x * disease_values_len) for x
                                                  in DISEASE_BOUNDARIES[disease['name']]]
        return statistics, diseases_boundaries

    def update_disease_average_cases(self):
        for disease in self.resources_manager.get_all_diseases():
            avg = 0.0
            for statistic in disease['statistics']:
                avg += statistic['total_number_cases']
            disease['avg_cases'] = avg / len(disease['statistics'])
            self.resources_manager.update_disease_metadata(disease)

    def get_diseases_codification(self):
        used_diseases = self.resources_manager.get_used_diseases()
        sorted_used_diseases_names = sorted([disease['name'] for disease in used_diseases])

        used_diseases_indexes = self.compute_element_index_codification(
            sorted_used_diseases_names)
        return used_diseases_indexes


if __name__ == '__main__':
    sm = Statistics_Manager()
    rm = Resources_Manager()
    print 'Computing average'
    # sm.update_disease_average_cases()
    print 'Done'
    # sm.create_statistics_for_diseases()
