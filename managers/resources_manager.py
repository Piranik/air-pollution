from managers.controllers.database_controller import Database_Controller


class Resources_Manager(object):
    """Resources Manager for Stations"""
    def __init__(self, app_config):
        super(Resources_Manager, self).__init__()
        self.app_config = app_config
        database_controller = Database_Controller()
        self.stations_collection = database_controller.get_collection('air_stations')
        self.parameters_collection = database_controller.get_collection('parameters')
        self.diseases_collection = database_controller.get_collection('diseases')
        self.counties_collection = database_controller.get_collection('counties')
        self.database_controller = database_controller

    # County Methos
    def add_county(self, new_county_name):
        county_query = self.county_query_object(new_county_name)
        county_update = self.county_update_object(new_county_name)
        self.counties_collection.update(county_query, county_update, True)

    def get_counties(self):
        return list(self.database_controller.find_in_collection(self.counties_collection.name, {}))

    # Disease Methods
    def update_insert_disease(self, new_disease, county, start_date, end_date):
        disease_query = self.disease_query_object(new_disease)
        disease_update = self.disease_update_object(new_disease, county, start_date, end_date)
        self.diseases_collection.update(disease_query, disease_update, True)

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
                new_station['internationalCode'], 'station_measurement')

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

    def get_stations_by_county(self, county_name):
        return list(self.database_controller.find_in_collection(self.stations_collection.name,
                                                                {'county': county_name}))

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

    # Disease query objects
    def disease_query_object(self, new_disease):
        return {
            'code': new_disease['code'],
            'type': new_disease['type']
            }

    def disease_update_object(self, new_disease, county, start_date, end_date):
        new_disease = self.convert_disease_object(new_disease, county, start_date, end_date)
        new_statistics = list(new_disease.pop('statistics'))
        return {'$set' : new_disease,
                '$push': {'statistics': {'$each': new_statistics}}}

    def convert_disease_object(self, new_disease, county, start_date, end_date):
        statistic_object = {'start_date': start_date,
                            'end_date': end_date,
                            'county': county,
                            'vr': new_disease['vr'],
                            'total_number_cases': new_disease['total_number_cases'],
                            'percentage_of_cases': new_disease['percentage_of_cases'],
                            'acute_casses': new_disease['acute_casses'],
                            'chronic_cases': new_disease['chronic_cases'],
                            'spitalization_total': new_disease['spitalization_total'],
                            'spitalization_acute': new_disease['spitalization_acute'],
                            'spitalization_chronic': new_disease['spitalization_chronic'],
                            'dms_acute': new_disease['dms_acute'],
                            'dms_chronic': new_disease['dms_chronic']
                           }
        converted_disease_object = {'name': new_disease['name'],
                                    'type': new_disease['type'],
                                    'code': new_disease['code'],
                                    'statistics': [statistic_object]}
        return converted_disease_object


    def county_query_object(self, county_name):
        return {'name': county_name}

    def county_update_object(self, county_name):
        return {'$set' : {'name' : county_name}}

