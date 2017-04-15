from config_utils.config import ConfigYaml
from managers.controllers.database_controller import Database_Controller
from bson.objectid import ObjectId

def _parameter_data_guard(parameters):
    if isinstance(parameters, list) or isinstance(parameters, set):
        return [int(parameter) for parameter in parameters]
    elif isinstance(parameters, dict):
        parameters['index'] = int(parameters['index'])
        return parameters


def _convert_objectId(document):
    document['_id'] = str(document['_id'])
    return document

def _set_objectId(document):
    if '_id' in document:
        document['_id'] = ObjectId(document['_id'])
    return document

class Resources_Manager(object):
    """Resources Manager for Stations"""
    def __init__(self, app_config=None):
        super(Resources_Manager, self).__init__()

        if not app_config:
            app_config = ConfigYaml().get_config()

        database_controller = Database_Controller()
        self.stations_collection = database_controller.get_collection('air_stations')
        self.parameters_collection = database_controller.get_collection('parameters')
        self.diseases_collection = database_controller.get_collection('diseases')
        self.counties_collection = database_controller.get_collection('counties')
        self.stations_statistics_collection = database_controller.get_collection(
            'air_stations_statistics')
        self.database_controller = database_controller

    # County Methos
    def add_county(self, new_county_name):
        county_query = self.county_query_object(new_county_name)
        county_update = self.county_update_object(new_county_name)
        self.counties_collection.update(county_query, county_update, True)

    def get_counties(self):
        counties = self.database_controller.find_in_collection(self.counties_collection.name, {})
        return [_convert_objectId(x) for x in counties]

    # Disease Methods
    def update_insert_disease(self, new_disease, county, start_date, end_date):
        disease_query = self.disease_query_object(new_disease)
        disease_update = self.disease_update_object(new_disease, county, start_date, end_date)
        self.diseases_collection.update(disease_query, disease_update, True)

    # Statistics air stations
    def get_stations_statistics(self):
        return list(self.database_controller.find_in_collection(
            self.stations_statistics_collection.name, {}))

    def update_insert_station_statistics(self, used_station):
        query_object = {'internationalCode': used_station['internationalCode']}
        self.database_controller.update_object_in_collection(
            self.stations_statistics_collection.name, {'$set': used_station},
            query_object, True)

    # Station methods
    def update_insert_station(self, new_station):
        station_parameters = []
        if 'parameters' in new_station:
            # Data guards
            station_parameters = _parameter_data_guard(new_station.pop('parameters'))
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

    def update_station_parameters(self, station_name, new_parameters):
        # Data guard
        new_parameters = _parameter_data_guard(new_parameters)

        self.stations_collection.update(
            {'internationalCode' : station_name},
            {'$addToSet' : {'parameters' :  {'$each': new_parameters}}}
        )

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
        # Data guard
        new_parameter = _parameter_data_guard(new_parameter)
        query_object = {
            'index': new_parameter['index']
        }
        self.database_controller.update_object_in_collection(
            self.parameters_collection.name, {'$set': new_parameter}, query_object, True)

    def update_insert_parameters(self, new_parameters):
        for new_parameter in new_parameters:
            self.update_insert_parameter(new_parameter)

    def mark_parameter_used(self, parameter):
        parameter['used'] = True
        _set_objectId(parameter)
        self.update_insert_parameter(parameter)

    def mark_parameter_viewed(self, parameter):
        parameter['view'] = True
        _set_objectId(parameter)
        self.update_insert_parameter(parameter)

    def get_parameter(self, parameter_index):
        return list(self.database_controller.find_in_collection(self.parameters_collection.name, {'index': str(parameter_index)}))[0]

    def get_used_parameters(self):
        used_parameters = self.database_controller.find_in_collection(
            self.parameters_collection.name, {'used': True})
        return list(_convert_objectId(x) for x in used_parameters)

    def get_viewed_parameters(self):
        used_parameters = self.database_controller.find_in_collection(
            self.parameters_collection.name, {'view': True})
        return list(_convert_objectId(x) for x in used_parameters)

    def get_all_parameters(self):
        parameters = self.database_controller.find_in_collection(self.parameters_collection.name,
                                                                 {})
        return [_convert_objectId(x) for x in parameters]

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

    def get_measurements_for_station(self, station_name, year=None, month=None,
        parameter_index=None):
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
            query_object['parameter_index'] = parameter_index
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

    def remove_stations(self):
        stations = self.get_stations()
        for station in stations:
            self.database_controller.drop_collection(station['internationalCode'])
        self.database_controller.drop_collection(self.stations_collection.name)

    def remove_parameters(self):
        self.database_controller.drop_collection(self.parameters_collection.name)
