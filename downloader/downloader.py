import urllib2
import re
import os
import shutil

from ckan_crawl.ckan_crawl import CrawlCKAN

FIRST_YEAR = 2009
LAST_YEAR = 2016

def _make_http_call(link):
    try:
        response = urllib2.urlopen(link)
        return response.getcode(), response.read()
    except urllib2.HTTPError as http_error:
        return http_error, None

class Donwloader(object):
    def __init__(self, config):
        super(Donwloader, self).__init__()
        self.config = config
        self.ckan_crawler = CrawlCKAN(config)
        print config
        self.disease_file_matcher = re.compile('.* href="([\w\d_\.]+)".*')
        self.folder_names = [self.config['diseases_folder'],
                             self.config['stations_measurements_folder']]

    def prepare_environment(self):
        for folder_name in self.folder_names:
            if not os.path.isdir(folder_name):
                os.makedirs(folder_name)

    def clear_environment(self):
        for folder_name in self.folder_names:
            if os.path.isdir(folder_name):
                shutil.rmtree(folder_name)

    def download_disease_files(self, link):
        code, response = _make_http_call(link)
        if code == 200:
            response_lines = response.split('\n')
            print 'SUCCESS: %s' % link
            for line in response_lines:
                file_match = self.disease_file_matcher.match(line)
                if file_match:
                    filename = file_match.group(1)
                    if 'xls' in filename:
                        self.download_disease_file(link, file_match.group(1))
            return True
        print 'FAIL: %s' % link
        return False


    def download_disease_file(self, link, filename):
        _, content = _make_http_call(link + filename)
        filepath = self.folder_names[0] + filename
        with open(filepath, 'wb') as disease_file:
            disease_file.write(content)


    def download_diseases(self):

        regex_pattern = '.* alt="\[(\w{3})\]".*>(\d{2})_(\d{4})/'
        regex_matcher = re.compile(regex_pattern)

        for year in range(FIRST_YEAR, LAST_YEAR+1):
            link = 'http://drg.ro/inc/%d/' % year
            code, response = _make_http_call(link)
            if code == 200:
                response_lines = response.split('\n')
                months = set()
                for line in response_lines:
                    regex_match = regex_matcher.match(line)
                    if regex_match:
                        if regex_match.group(1) == 'DIR':
                            month = regex_match.group(2)
                            months.add(month)

                for month in months:
                    new_link = ('http://drg.ro/inc/%d/%s_%d/DRG/' +
                                '02_Judet_pacient/') % (year, month, year)
                    ret = self.download_disease_files(new_link)
                    if not ret:
                        new_link = ('http://drg.ro/inc/%d/%s_%d/DRG/' +
                                    '02_Judet%%20pacient/') % (year, month, year)
                        self.download_disease_files(new_link)
            print ''


    def download_stations(self):
        self.ckan_crawler.do_process_all()

