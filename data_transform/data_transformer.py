from managers.resources_manager import Resources_Manager
from data_summary import create_summary_for_used_stations

_YEARS = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
_MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
_MIN_PARAMETER_COUNT = 100


class Data_Transformer(object):
    def __init__(self, app_config):
        super(Data_Transformer, self).__init__()
        self.resources_manager = Resources_Manager(app_config)
        self.parameters = self.resources_manager.get_all_parameters()


    def transform_data_for_station(self, station, common_parameters):
        for year in _YEARS.reverse():
            for month in _MONTHS:
                for parameter in common_parameters:
                    measurements = self.resources_manager.get_measurementes_for_station(station['internationalCode'], year, month)

    def transform_data(self):
        stations = self.resources_manager.get_stations()
        common_parameters = self.find_common_parameters(stations)
        common_stations = self.find_common_stations(common_parameters)
        print common_stations
        print len(common_stations)

        used_parameters = [parameter for parameter in self.parameters
                           if parameter['index'] in common_parameters]

        used_stations = [station for station in stations
                         if station['internationalCode'] in common_stations]
        create_summary_for_used_stations(used_stations, used_parameters,
                                         self.resources_manager)
        # for station in stations:
        #     transform_data_for_station(station)


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
                print parameter['index']
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
            if station not in common_stations:
                if self.check_valid_station(station, common_parameters):
                    common_stations.add(station)

        return common_stations


    def check_valid_station(self, station, common_parameters):
        ok_flag = True
        for parameter_index in common_parameters:
            if station not in common_parameters[parameter_index]:
                ok_flag = False

        return ok_flag
