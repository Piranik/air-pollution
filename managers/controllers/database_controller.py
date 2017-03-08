import sys
from pymongo import MongoClient, ASCENDING

DEFAULT_STATION_INDEXES = [
    ('year', ASCENDING),
    ('month', ASCENDING),
    ('time', ASCENDING),
    ('parameter_index', ASCENDING)
]

DEFAULT_PARAMETER_INDEXES = [
    # ('formula', ASCENDING),
    # ('name', ASCENDING),
    ('index', ASCENDING)
]

DEFAULT_STATION_COLLECTION_INDEXES = [
    ('internationalCode', ASCENDING)
]

DEFAULT_DISEASES_COLLECTION_INDEXES = [
    ('code', ASCENDING),
    ('name', ASCENDING),
    ('type', ASCENDING)
]

DEFAULT_COUNTIES_COLLECTION_INDEXES = [
    ('name', ASCENDING)
]


class Database_Controller(object):

    def __init__(self, url = 'mongodb://localhost/', port=27017, database='Air-Pollution'):
        self.db_connection = MongoClient(url + str(port))
        self.database = self.db_connection[database]
        self.create_initial_collections()
        self.collections = set(self.database.collection_names())

    def create_initial_collections(self):
        current_collections = self.database.collection_names()
        if 'air_stations' not in current_collections:
            air_stations_collection = self.database.create_collection('air_stations')
            air_stations_collection.create_index(DEFAULT_STATION_COLLECTION_INDEXES, unique=True)
        if 'parameters' not in current_collections:
            parameters_collection = self.database.create_collection('parameters')
            parameters_collection.create_index(DEFAULT_PARAMETER_INDEXES, unique=True)
        if 'diseases' not in current_collections:
            diseases_collection = self.database.create_collection('diseases')
            diseases_collection.create_index(DEFAULT_DISEASES_COLLECTION_INDEXES, unique=True)
        if 'counties' not in current_collections:
            counties_collection = self.database.create_collection('counties')
            counties_collection.create_index(DEFAULT_COUNTIES_COLLECTION_INDEXES, unique=True)

    def check_connection(self):
        return self.db_connection['connect']

    def get_collection(self, collection_name):
        return self.database[collection_name]

    def collection_exists(self, collection_name):
        return collection_name in self.collections

    def create_collection(self, name, mode=None):
        new_collection = self.database.create_collection(name)

        if new_collection:
            self.collections.add(name)
            if mode == 'station':
                new_collection.create_index(DEFAULT_STATION_COLLECTION_INDEXES, unique=True)
            elif mode == 'parameter':
                new_collection.create_index(DEFAULT_PARAMETER_INDEXES, unique=True)
            elif mode == 'county':
                new_collection.create_index(DEFAULT_COUNTIES_COLLECTION_INDEXES, unique=True)
            elif mode == 'station_measurement':
                new_collection.create_index(DEFAULT_STATION_INDEXES, unique=True)
            elif mode == 'disease':
                new_collection.create_index(DEFAULT_DISEASES_COLLECTION_INDEXES, unique=True)

        return new_collection

    def insert_object_in_collection(self, collection_name, new_object):
        self.database[collection_name].insert(new_object)

    def update_object_in_collection(self, collection_name, new_object, update_query, upsert=False):
        self.database[collection_name].update_one(update_query,
            new_object, upsert)

    # Find methods
    def find_in_collection(self, collection_name, query_object):
        return self.database[collection_name].find(query_object)
