import urllib2
import re
import os

STORAGE_FOLDERS = {
    'diseases': 'diseases_all/',
    'stations': 'datasets_all/'
}

def make_http_call(link):
    try:
        response = urllib2.urlopen(link)
        return response.getcode(), response.read()
    except urllib2.HTTPError as http_error:
        return http_error, None

def prepare_environment(mode):
    folder_name = STORAGE_FOLDERS[mode]
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)


def download_diseases():
    FIRST_YEAR = 2009
    LAST_YEAR = 2016

    regex_pattern = '.* alt="\[(\w{3})\]".*>(\d{2})_(\d{4})/'
    regex_matcher = re.compile(regex_pattern)

    prepare_environment('diseases')

    for year in range(FIRST_YEAR, LAST_YEAR+1):
        link = 'http://drg.ro/inc/%d/' % year
        code, response = make_http_call(link)
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
                            '03_Judet_Spital/') % (year, month, year)
                ret = download_disease_files(new_link)
                if not ret:
                    new_link = ('http://drg.ro/inc/%d/%s_%d/DRG/' +
                                '03_Judet%%20Spital/') % (year, month, year)
                    download_disease_files(new_link)
        print ''

def download_disease_files(link):
    code, response = make_http_call(link)

    if code == 200:
        response_lines = response.split('\n')
        disease_file_pattern = '.* href="([\w\d_\.]+)".*'
        file_matcher = re.compile(disease_file_pattern)
        print 'SUCCESS: %s' % link
        for line in response_lines:
            file_match = file_matcher.match(line)
            if file_match:
                filename = file_match.group(1)
                if 'xls' in filename:
                    write_file(link, file_match.group(1))
        return True
    print 'FAIL: %s' % link
    return False

def write_file(link, filename):
    _, content = make_http_call(link + filename)
    filepath = STORAGE_FOLDERS['diseases'] + filename
    with open(filepath, 'wb') as disease_file:
        disease_file.write(content)

if __name__ == '__main__':
    download_diseases()
