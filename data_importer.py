import sys
import os
from os import listdir
from os.path import isfile, join

from database_controller import Database_Controller
from xls_parser import Xls_Parser
from xml_parser import Xml_Parser
from resources_manager import Resources_Manager
from xml.etree.ElementTree import ParseError


FILES = {
    'stations': 'data_files/informatii-privind-statiile-rnmca.xls',
    'parsed_sets': 'datasets',
    'all_sets': 'datasets_all'
}

def write_error_in_log(file_name):
    with open('error_measurements.log', 'a') as error_measurements_log:
        error_measurements_log.write(file_name + '\n')

if __name__== '__main__':
    # ensure db connection
    database_controller = Database_Controller()
    if database_controller.check_connection():
        print 'Database connection .... Success'
    else:
        print 'Database connection .... Fail'
        sys.exit(1)

    resources_manager = Resources_Manager(database_controller)
    xls_parser = Xls_Parser(FILES['stations'])
    xml_parser = Xml_Parser()

    stations = xls_parser.parse()

    for station in stations:
        resources_manager.update_insert_station(station)

    datasets_files = [join(FILES['all_sets'], f) for f in listdir(FILES['all_sets']) if isfile(join(
        FILES['all_sets'], f)) and '.xml' in f]

    for dataset_file in datasets_files:
        try:
            print 'Parsing: %s' % dataset_file
            station_info, date, measurements = xml_parser.parse_file(dataset_file)
            if measurements is None or station_info is None:
                write_error_in_log(dataset_file)
            else:
                print 'Adding resources'
                resources_manager.add_measurements_for_station(dataset_file, station_info, date, measurements)
            print 'File %s Succesful' % dataset_file
        except ParseError as parse_error:
            write_error_in_log(dataset_file)


