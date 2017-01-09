import sys

from mongo_database import Mongo_Database
from xls_parser import Xls_Parser
from stations_collection import Stations_collection


FILES = {
	'stations': 'data_files/informatii-privind-statiile-rnmca.xls'
}

if __name__== '__main__':

	# ensure db connection
	database = Mongo_Database()
	if database.check_connection():
		print 'Database connection .... Success'
	else:
		print 'Database connection .... Fail'
		sys.exit(1)

	stations_collection = Stations_collection()


	stations_parser = Xls_Parser(FILES['stations'])
	stations = stations_parser.parse()

	for station in stations:
		stations_collection.update_insert_station(station)

