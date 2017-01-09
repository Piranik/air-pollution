from pymongo import MongoClient
from singleton import Singleton


class Mongo_Database(object):
	__metaclass__ = Singleton

	def __init__(self, url = 'mongodb://localhost/', port=27017, database='Air-Pollution'):
		self.db_connection = MongoClient(url + str(port))
		self.database = self.db_connection[database]

	def check_connection(self):
		return self.db_connection['connect']


	def get_collection(self, collection_name):
		return self.database[collection_name]


	def insert_object_in_collection(self, object, collection_name):
		self.database[collection_name].insert()

	def update_object_in_collection(self, collection_name, object, update_query, upsert=False):
		self.database[collection_name].update_one(update_query, object, upsert)



if __name__ == '__main__':
	mongo_cls = Mongo_Database("url", "db")
	mongo_cl1 = Mongo_Database("url", "db")
	mongo_cl2 = Mongo_Database("url", "db")
	print id(mongo_cl1)
	print id(mongo_cl2)
	print id(mongo_cls)
	print 'e bine ?'

