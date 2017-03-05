from ckanapi import RemoteCKAN
import dateutil.parser
from datetime import datetime

import requests
import json
import re
import copy
import os

ORGANIZATION_NAME = 'agentia-nationala-pentru-protectia-mediului'
DOWNLOAD_FOLDER = '../datasets/'
OTHER_DOWNLOAD_FOLDER = '../other_files/'

DOWNLOAD_FOLDER_ALL = '../datasets_all/'


class CrawlCKAN(object):
    def __init__(self,config):
        self.config = config
        self.current_time = datetime.now()
        self.ckan_inst = RemoteCKAN(address=self.config["ckan"]["url"],
                                    apikey='47cfc9c5-451e-4d6c-9731-e59d985e74ae')
        self.ckan_time = self.config["ckan"]["last_modified"]

        self.resources_metadata = []
        self.other_resources = []
        self.resources_fetched_files = 0

        self.prepare_environment()


    def do_process_all(self):
        print "BEGIN PROCESSING DATASETS METADATA " + str(self.current_time)
        offset = 0
        limit_size = received = 100
        file_index = 0
        while limit_size == received:
            datasets = self.ckan_inst.action.current_package_list_with_resources(
                limit=limit_size, offset=offset)
            received = len(datasets)
            offset += received

            datasets = self.filter_datasets(datasets)
            for dataset in datasets:
                for resource in dataset['resources']:
                    response = self.download_resource_data(resource['url'])
                    filename = (DOWNLOAD_FOLDER_ALL + 'resource' +
                                str(file_index) + '.' + resource['format'].lower())
                    if os.path.isfile(filename):
                        continue
                    self.write_file(filename, response.content)
                    file_index += 1

    def do_process_selective(self):
        print "BEGIN PROCESSING DATASETS METADATA " + str(self.current_time)
        offset = 0
        limit_size = received = 100

        while limit_size == received:
            datasets = self.ckan_inst.action.current_package_list_with_resources(
                limit=limit_size, offset=offset)
            received = len(datasets)
            offset += received

            datasets = self.filter_datasets(datasets)
            for dataset in datasets:
                self.process_dataset(dataset)

        print "END PROCESSING DATASETS METADATA " + str(self.current_time)

        total_resources = len(self.resources_metadata)
        print "DONWLOADING RESOURCES: %d" % total_resources
        self.download_resources()
        self.download_other_resources()
        print "DONWLOADING FINISHED: %d / %d" % (self.resources_fetched_files, total_resources)
        print "FOUND OTHER RESOURCES IN RESOURCES: %d" % len(
            self.other_resources)

    def process_dataset(self, dataset):
        name = month = year = None
        for resource in dataset['resources']:
            try:
                self.convert_text(resource)
                name, month, year = self.parse_metadata(resource)
                name = self.convert_name(name)
                year = self.convert_year(year)
                if len(name) < 7:
                    self.other_resources.append(resource)
                else:
                    self.resources_metadata.append({'name': name,
                                                    'month': month,
                                                    'year': year,
                                                    'url': resource['url'],
                                                    'format': resource['format']})
            except AttributeError:
                self.other_resources.append(resource)

    def filter_datasets(self, datasets):
        return [x for x in datasets if
                x['organization']['name'] == ORGANIZATION_NAME and
                dateutil.parser.parse(x["metadata_modified"]) > self.ckan_time]


    def parse_metadata(self, resource):
        name_pattern = re.compile('.*(ro\d+\w?|statia_\d+).*')
        month_pattern = re.compile('.*(ianuarie|februarie|martie|aprilie|mai|'
                                   + 'iunie|iulie|august|septembrie|'
                                   + 'octombrie|noiembrie|decembrie).*')
        year_pattern = re.compile('.*[\s|_]+(\d{4})|anul-\d{4}.*')

        found_name = found_month = found_year = None

        if 'name' in resource and resource['name']:
            found_name = name_pattern.match(resource['name'])
            found_year = year_pattern.match(resource['name'])
            found_month = month_pattern.match(resource['name'])

        if 'title' in resource and resource['title']:
            if not found_name:
                found_name = name_pattern.match(resource['title'])
            if not found_year:
                found_year = year_pattern.match(resource['title'])
            if not found_month:
                found_month = month_pattern.match(resource['title'])

        if 'description' in resource and resource['description']:
            if not found_name:
                found_name = name_pattern.match(resource['description'])
            if not found_year:
                found_year = year_pattern.match(resource['description'])
            if not found_month:
                found_month = month_pattern.match(resource['description'])

        return found_name.group(1), found_month.group(1), found_year.group(1)

    def download_other_resources(self):
        for other_resource in self.other_resources:
            last_index = other_resource['url'].rindex('/')
            filename = OTHER_DOWNLOAD_FOLDER + other_resource['url'][last_index+1:]
            response = self.download_resource_data(other_resource['url'])
            self.write_file(filename, response.content)

    def download_resources(self):
        for resource in self.resources_metadata:
            #download file in folder
            filename = (DOWNLOAD_FOLDER + resource['name'] + '_'
                        + resource['month'] + '_' + resource['year'] + '.'
                        + resource['format'].lower())
            if os.path.isfile(filename):
                continue
            response = self.download_resource_data(resource['url'])
            if response.status_code == 200:
                self.write_file(filename, response.content)
            else:
                with open('error.log', 'a') as error_log:
                    error_log.write('Exceptie\n')
                    error_log.write(
                        'URL: %s came with status: %d\n\n' % (
                            resource['url'], response.status_code))

    def write_file(self, filename, content):
        try:
            with open(filename, 'wb') as output:
                output.write(content)
            self.resources_fetched_files += 1
            print '%s was downloaded successfully' % filename
        except IOError:
            return False
        return True

    def download_resource_data(self, url):
        return requests.get(url)

    def convert_text(self, resource):
        if 'title' in resource:
            resource['title'] = resource['title'].encode('ascii', 'ignore').lower()
        if 'name' in resource:
            resource['name'] = resource['name'].encode('ascii', 'ignore').lower()

        if 'description' in resource:
            resource['description'] = resource['description'].encode('ascii', 'ignore').lower()

    #convert statia_XXX to ROXXXXa
    def convert_name(self, name):
        if 'statia' in name:
            index_of_underscore = name.index('_')
            return 'RO' + ('0000' + name[index_of_underscore+1:])[-4:] + 'A'
        return name.upper()

    def convert_year(self, year):
        if 'anul-' in year:
            index_of_line = year.rindex('-')
            print year
            return year[index_of_line+1:]
        return year


    def prepare_environment(self):
        if not os.path.isdir(DOWNLOAD_FOLDER):
            os.makedirs(DOWNLOAD_FOLDER)

        if not os.path.isdir(OTHER_DOWNLOAD_FOLDER):
            os.makedirs(OTHER_DOWNLOAD_FOLDER)

        if not os.path.isdir(DOWNLOAD_FOLDER_ALL):
            os.makedirs(DOWNLOAD_FOLDER_ALL)

