import sys
import os
from os import listdir
from os.path import isfile, join

from database_controller import Database_Controller
from stations_info_parser import StationsInfoParser
from xml_parser import Xml_Parser
from rdf_parser import RDF_Parser
from resources_manager import Resources_Manager
from xml.etree.ElementTree import ParseError


FILES = {
    'stations': 'data_files/informatii-privind-statiile-rnmca.xls',
    'counties_stations_distribution':
        'informatii-privind-repartizarea-statiilor-rnmca-pe-zone-si-aglomerari.xls',
    'parsed_sets': 'datasets',
    'all_sets': 'datasets_all'
}

def write_error_in_log(file_name):
    with open('error_measurements.log', 'a') as error_measurements_log:
        error_measurements_log.write(file_name + '\n')


def check_db_connection(database_controller):
    if database_controller.check_connection():
        print 'Database connection .... Success'
    else:
        print 'Database connection .... Fail'
        sys.exit(1)


def import_data():
     # ensure db connection
    database_controller = Database_Controller()
    check_db_connection(database_controller)
    resources_manager = Resources_Manager(database_controller)
    stations_info_parser = StationsInfoParser()
    xml_parser = Xml_Parser()
    rdf_parser = RDF_Parser()

    stations, county_stations_organization = stations_info_parser.parse(FILES['stations'], FILES['counties_stations_distribution'])

    # update stations
    for county in county_stations_organization:
        for station_code in county_stations_organization[county]:
            stations[station_code]['county'] = county
    print stations
    for station_code in stations:
        print station_code
        resources_manager.update_insert_station(stations[station_code])

    # counties_locality_graph = rdf_parser.parse(FILES['counties_locality'])
    # for station in stations:
    #     station['location'] = station['location'].lower()
    #     print (station['internationalCode'], station['location'])
    #     for county in counties_locality_graph:
    #         if station['location'] in counties_locality_graph[county]:
    #             counties_locality_graph[county][station['location']].append(
    #                 station['internationalCode'])
    #             print (county, station['location'])
    #             print '\n'
    #             break
    # print counties_locality_graph['neamt']
    # for station in stations:
    #     print station
    #     resources_manager.update_insert_station(station)

    # # Parse stations
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
                if resources_manager.station_exists(station_info['internationalCode']):
                    resources_manager.add_measurements_for_station(
                        dataset_file, station_info, date, measurements)
            print 'File %s Succesful' % dataset_file
        except ParseError:
            write_error_in_log(dataset_file)


if __name__ == '__main__':
    import_data()

