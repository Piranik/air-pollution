from database_controller import DEFAULT_STATION_COLLECTION_INDEXES, DEFAULT_PARAMETER_INDEXES, DEFAULT_STATION_INDEXES


files = ['data_files/informatii-privind-statiile-rnmca.xls']

station_key = 'statia'

class Resources_Manager(object):
    """Resources Manager for Stations"""
    def __init__(self, database_controller):
        super(Resources_Manager, self).__init__()
        self.database_controller = database_controller
        self.stations_collection = database_controller.get_collection('air_stations')
        self.parameters_collection = database_controller.get_collection('parameters')

    # Station methods
    def update_insert_station(self, new_station):
        station_parameters = []
        if 'parameters' in new_station:
            station_parameters = list(new_station.pop('parameters'))
        self.stations_collection.update(
            {'internationalCode' : new_station['internationalCode']},
            {
                '$set': new_station,
                '$addToSet' : {'parameters' : {
                    '$each': station_parameters}
                              }
            }, upsert=True)

        if not self.database_controller.collection_exists(
                new_station['internationalCode']):
            self.database_controller.create_collection(
                new_station['internationalCode'], DEFAULT_STATION_INDEXES)

    def update_station(self, new_station):
        station_collection = self.database_controller.get_collection(
            new_station['internationalCode'])
        if station_collection:
            station_collection.update(
                {'internationalCode': new_station['internationalCode']},
                new_station)

    def station_exists(self, station_name):
        station = None
        station_collection_query = {
            'internationalCode': station_name
        }
        station_cursor = self.database_controller.find_in_collection(
            self.stations_collection.name, station_collection_query)
        if station_cursor.count() > 0:
            station = station_cursor[0]

        return station is not None and self.database_controller.collection_exists(station_name)


    # Parameter methods
    def update_insert_parameter(self, new_parameter):
        query_object = {
            'index': new_parameter['index']
        }
        self.database_controller.update_object_in_collection(
            self.parameters_collection.name, {'$set': new_parameter}, query_object, True)

    def update_insert_parameters(self, new_parameters):
        for new_parameter in new_parameters:
            self.update_insert_parameter(new_parameter)

    def get_parameter(self, parameter_index):
        return list(self.database_controller.find_in_collection(self.parameters_collection.name, {'index': str(parameter_index)}))[0]

    def get_all_parameters(self):
        return list(self.database_controller.find_in_collection(self.parameters_collection.name, {}))

    # Get Methods
    def get_stations(self):
        stations = self.database_controller.find_in_collection('air_stations', {})
        return list(stations)

    # Measurement methods
    # Add/Update Methods
    def insert_measurement(self, station_code, parameter_info, parameter_measurements, date, filename):
        query_object = self.create_station_query_object(date, parameter_info)
        station_new_measurements_object = self.create_station_object(
            filename, date, parameter_info, parameter_measurements)
        self.database_controller.update_object_in_collection(
            station_code, station_new_measurements_object, query_object, True)

    def add_measurements_for_station(self, file_name, station, date, measurements):
        # Check station
        # if self.database_controller.collection_exists(station['internationalCode']):
        for parameter_info, parameter_measurements in measurements:
            self.update_insert_parameter(parameter_info)
            self.insert_measurement(station['internationalCode'],
                                    parameter_info, parameter_measurements, date, file_name)

    def get_measurements_for_station(self, station_name, year=None,
        month=None, parameter_index=None):
        if self.database_controller.collection_exists(station_name):
            query_object = self.create_query_object_for_find(year, month, parameter_index)
            measurements = self.database_controller.find_in_collection(station_name, query_object)
            return list(measurements)
        return None


    def create_query_object_for_find(self, year=None, month=None, parameter_index=None):
        query_object = {}
        if year:
            query_object['year'] = str(year)

        if month:
            query_object['month'] = str(month)

        if parameter_index:
            query_object['parameter_index'] = str(parameter_index)
        return query_object

    def create_station_query_object(self, date, parameter):
        date_index_of_line = date.find('-')
        return {
            'parameter_index': parameter['index'],
            'year': date[0:date_index_of_line],
            'month': date[date_index_of_line+1:]}


    def create_station_object(self, file_name, date, parameter, measurements):
        date_index_of_line = date.find('-')
        return {'$set': {
            'file_name': file_name,
            'parameter_index': parameter['index'],
            'year': date[0:date_index_of_line],
            'month': date[date_index_of_line+1:],
            'measurements': measurements}}
