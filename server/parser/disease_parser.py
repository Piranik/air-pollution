from xls_parser import Xls_Parser
import re

START_ROW = 14
OBJECT_PARAMETERS_CASE1 = {
    'code': 3, 'name': 5, 'type': 6, 'vr': 8,
    'total_number_cases': 9, 'percentage_of_cases': 10,
    'acute_casses': 12, 'chronic_cases': 14,
    'spitalization_total': 16, 'spitalization_acute': 18,
    'spitalization_chronic': 20, 'dms_acute': 22,
    'dms_chronic': 23}

OBJECT_PARAMETERS_CASE2 = {
    'code': 3, 'name': 5, 'type': 7, 'vr': 9,
    'total_number_cases': 10, 'percentage_of_cases': 11,
    'acute_casses': 13, 'chronic_cases': 15,
    'spitalization_total': 17, 'spitalization_acute': 21,
    'spitalization_chronic': 23, 'dms_acute': 25,
    'dms_chronic': 26}

# This parameter is index of G which if it's an empty
# cell then it's second obj params else it's first.
DIFFERENCE_COL = 6

class Disease_parser(object):
    def __init__(self):
        super(Disease_parser, self).__init__()
        self.name_pattern = re.compile('.*___(\w+)___(\d+\.\d+\.\d+)_(\d+\.\d+\.\d+).*')

    def parse(self, filename):
        print filename
        county, start_date, end_date = self.parse_metadata(filename)
        xls_parser = Xls_Parser(filename)
        nr_rows, _ = xls_parser.get_sheet_dimension()
        disease_objects = []

        for row in range(START_ROW, nr_rows):
            ok_flag, disease_object = self.read_row(xls_parser, row)
            if ok_flag:
                disease_objects.append(disease_object)
        return county, start_date, end_date, disease_objects

    def parse_metadata(self, filename):
        match = self.name_pattern.match(filename)
        if match:
            return match.group(1).lower(), match.group(2), match.group(3)
        return None, None, None

    def read_value(self, xls_parser, x, y):
        value = xls_parser.get_value(x, y)
        if value != None:
            if type(value).__name__ == 'unicode':
                value = value.replace(u'\xe2', 'a')
                return str(value)
            return value
        return None

    def read_row(self, xls_parser, row_number):
        disease_object = {}
        row_with_data_flag = self.read_value(xls_parser, row_number, OBJECT_PARAMETERS_CASE1['code'])
        if row_with_data_flag:
            if self.read_value(xls_parser, row_number, DIFFERENCE_COL):
                obj_params = OBJECT_PARAMETERS_CASE1
            else:
                obj_params = OBJECT_PARAMETERS_CASE2

            for param in obj_params:
                value = self.read_value(xls_parser, row_number, obj_params[param])
                disease_object[param] = value
        return row_with_data_flag, disease_object


if __name__ == '__main__':
    x = Disease_parser().parse('../diseases_all/IM_DRG___VRANCEA___1.4.2012_30.4.2012.xls')

