from mongo_database import Mongo_Database

files = ['data_files/informatii-privind-statiile-rnmca.xls']

main_key = 'statia'

class Stations_collection(object):

	def __init__(self):
		self.collection = Mongo_Database().get_collection('air_stations')

	def update_insert_station(self, new_station):
		return self.collection.update({'statia' : new_station['statia']}, new_station, upsert=True)

	def update_station(self, new_station):
		self.collection.update({'statia': new_station['statia']}, new_station)

	def insert_station(self, new_station):
		self.collection.insert(new_station)

