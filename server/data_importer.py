import sys
import os
from os import listdir
from os.path import isfile, join
from xml.etree.ElementTree import ParseError

from managers.resources_manager import Resources_Manager
from managers.statistics_manager import Statistics_Manager

from parser.disease_parser import Disease_parser
from parser.stations_info_parser import StationsInfoParser
from parser.station_measurement_parser import StationMeasurementParser


def write_error_in_log(file_name):
    with open('error_measurements.log', 'a') as error_measurements_log:
        error_measurements_log.write(file_name + '\n')

def import_stations(resources_manager, app_config):
    print 'Importing Stations'

    stations_info_parser = StationsInfoParser()

    stations, county_stations_organization = stations_info_parser.parse(
        app_config['stations'], app_config['counties_stations_distribution'])

    # update stations
    for county in county_stations_organization:
        if county_stations_organization[county]:
            resources_manager.add_county(county)
            for station_code in county_stations_organization[county]:
                stations[station_code]['county'] = county

    for station_code in stations:
        print station_code
        resources_manager.update_insert_station(stations[station_code])
    print 'Importing Stations Done'


def import_stations_measurements(resources_manager, app_config):
    print 'Importing Measurements'
    # Parse stations
    station_measurement_parser = StationMeasurementParser()

    datasets_files = [join(app_config['stations_measurements_folder'], f) for f in listdir(
        app_config['stations_measurements_folder']) if isfile(join(
            app_config['stations_measurements_folder'], f)) and '.xml' in f]
    # print datasets_files
    for dataset_file in datasets_files:
        try:
            print 'Parsing: %s' % dataset_file
            station_info, date, measurements = station_measurement_parser.parse_file(dataset_file)
            # print station_info, date, len(measurements)
            if measurements is None or station_info is None:
                write_error_in_log(dataset_file)
            else:
                print 'Adding resources'
                if resources_manager.station_exists(
                        station_info['internationalCode']):
                    # resources_manager.update_insert_station()
                    resources_manager.update_station_parameters(
                        station_info['internationalCode'], station_info['parameters'])
                    resources_manager.add_measurements_for_station(
                        dataset_file, station_info, date, measurements)
            print 'File %s Succesful' % dataset_file
        except ParseError:
            write_error_in_log(dataset_file)
    print 'Importing Measurements'


def import_diseases(resources_manager, statistics_manager, app_config):
    print 'Importing Diseases'
    disease_parser = Disease_parser()
    # Parse disease files
    diseases_files = [join(app_config['diseases_folder'], f) for f in
                      listdir(app_config['diseases_folder']) if isfile(join(
                          app_config['diseases_folder'], f)) and '.xls' in f]

    diseases_storage = {}
    for disease_file in diseases_files:
        county, start_date, end_date, diseases = disease_parser.parse(disease_file)
        for disease in diseases:
            if disease['code'] in diseases_storage:
                updated_disease = diseases_storage[disease['code']]
                new_statistic = create_disease_statistic_object(disease, county, start_date,
                                                                end_date)
                updated_disease['statistics'].append(new_statistic)
            else:
                diseases_storage[disease['code']] = create_disease_object(disease, county, start_date, end_date)

        print county, start_date, end_date, len(diseases), len(diseases_storage)

    print 'Importing Diseases Done'
    for disease in diseases_storage:
        resources_manager.update_insert_disease(diseases_storage[disease])
    print 'Saving Diseases Done'
    print 'Computing average'
    statistics_manager.update_disease_average_cases()
    print 'Done'

def create_disease_statistic_object(new_disease, county, start_date, end_date):
    return {'start_date': start_date,
            'end_date': end_date,
            'county': county,
            'vr': new_disease['vr'],
            'total_number_cases': new_disease['total_number_cases'],
            'percentage_of_cases': new_disease['percentage_of_cases'],
            'acute_cases': new_disease['acute_cases'],
            'chronic_cases': new_disease['chronic_cases'],
            'spitalization_total': new_disease['spitalization_total'],
            'spitalization_acute': new_disease['spitalization_acute'],
            'spitalization_chronic': new_disease['spitalization_chronic'],
            'dms_acute': new_disease['dms_acute'],
            'dms_chronic': new_disease['dms_chronic']}

def create_disease_object(new_disease, county, start_date, end_date):
        statistic_object = create_disease_statistic_object(new_disease, county, start_date,
                                                           end_date)
        disease_object = {'name': new_disease['name'],
                          'type': new_disease['type'],
                          'code': new_disease['code'],
                          'statistics': [statistic_object]}
        return disease_object


def import_data(app_config):
    # ensure db connection
    resources_manager = Resources_Manager()
    statistics_manager = Statistics_Manager()
    # import_stations(resources_manager, app_config)
    # import_stations_measurements(resources_manager, app_config)
    import_diseases(resources_manager, statistics_manager, app_config)

