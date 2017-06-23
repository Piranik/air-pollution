from managers.resources_manager import Resources_Manager
from managers.statistics_manager import Statistics_Manager
from data_summary import create_summary_for_used_stations

_YEARS = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
_MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
_MIN_PARAMETER_COUNT = 100

_UNVIEWED_PARAMETERS = [23, 21, 18, 26, 10]
NO2_INDEX = 1001
NOx_INDEX = 3
NO_INDEX = 10


class Data_Transformer(object):
    def __init__(self, app_config):
        super(Data_Transformer, self).__init__()
        self.resources_manager = Resources_Manager(app_config)
        self.statistics_manager = Statistics_Manager()
        self.parameters = self.resources_manager.get_all_parameters()

    def transform_data(self):
        stations = self.resources_manager.get_stations()
        common_parameters = self.find_common_parameters(stations)
        common_stations = self.find_common_stations(common_parameters)

        # Remove NOx and NO and add NO2_INDEX and AQI
        del common_parameters[NOx_INDEX]
        del common_parameters[NO_INDEX]
        used_parameters = [parameter for parameter in self.parameters
                           if parameter['index'] in common_parameters]
        used_parameters.append({'name': 'Dioxid de azot', 'formula': 'NO2', 'index': NO2_INDEX})
        used_parameters.append({'name': 'Air Quality Index', 'formula': 'AQI', 'index': 2000})
        used_stations = [station for station in stations
                         if station['internationalCode'] in common_stations]
        used_stations_statistics = create_summary_for_used_stations(used_stations, used_parameters,
                                                                    self.resources_manager)

        self.save_used_parameters_and_stations(used_parameters, used_stations_statistics)
        self.statistics_manager.update_disease_average_cases()
        self.statistics_manager.create_statistics_for_diseases()

    def find_common_parameters(self, stations):
        common_parameters = {}
        parameters_codification = {}
        for parameter in self.parameters:
            common_parameters[parameter['index']] = set()
            parameters_codification[parameter['index']] = parameter['name']

        for parameter in self.parameters:
            for station in stations:
                if parameter['index'] in station['parameters']:
                    common_parameters[parameter['index']].add(station['internationalCode'])

        for parameter in self.parameters:
            if len(common_parameters[parameter['index']]) < _MIN_PARAMETER_COUNT:
                del common_parameters[parameter['index']]

        for parameter_index in common_parameters:
            print '%s -> %d' % (
                parameters_codification[parameter_index],
                len(common_parameters[parameter_index]))

        return common_parameters


    def find_common_stations(self, common_parameters):
        common_stations = set()
        all_possible_stations = set()

        for parameter_index in common_parameters:
            for station in common_parameters[parameter_index]:
                all_possible_stations.add(station)

        for station in all_possible_stations:
            if (station not in common_stations) and (self.check_valid_station(station, common_parameters)):
                common_stations.add(station)

        return common_stations


    def check_valid_station(self, station, common_parameters):
        ok_flag = True
        for parameter_index in common_parameters:
            if station not in common_parameters[parameter_index]:
                ok_flag = False

        return ok_flag

    def save_used_parameters_and_stations(self, used_parameters, used_stations):
        for parameter in used_parameters:
            self.resources_manager.mark_parameter_used(parameter)
            if parameter['index'] not in _UNVIEWED_PARAMETERS:
                self.resources_manager.mark_parameter_viewed(parameter)

        for station in used_stations:
            self.resources_manager.update_insert_station_statistics(station)
