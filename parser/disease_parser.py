from xls_parser import Xls_Parser
import re

START_ROW = 14
OBJECT_PARAMETERS = {'code': 3, 'name': 5, 'type': 6, 'vr': 8,
                     'total_number_cases': 9, 'percentage_of_cases': 10,
                     'acute_casses': 12, 'chronic_cases': 14,
                     'spitalization_total': 16, 'spitalization_acute': 18,
                     'spitalization_chronic': 20, 'dms_acute': 22,
                     'dms_chronic': 23}

class Disease_parser(object):
    def __init__(self):
        super(Disease_parser, self).__init__()
        self.name_pattern = re.compile('.*___(\w+)___(\d+\.\d+\.\d+)_(\d+\.\d+\.\d+).*')

    def parse(self, filename):
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
        if value:
            if type(value).__name__ == 'unicode':
                value = value.replace(u'\xe2', 'a')
                return str(value)
            return value
        return None

    def read_row(self, xls_parser, row_number):
        disease_object = {}
        row_with_data_flag = self.read_value(xls_parser, row_number, OBJECT_PARAMETERS['code'])
        for param in OBJECT_PARAMETERS:
            value = self.read_value(xls_parser, row_number, OBJECT_PARAMETERS[param])
            disease_object[param] = value
        return row_with_data_flag, disease_object


if __name__ == '__main__':
    Disease_parser().parse('diseases_all/IM_DRG___BUCURESTI___1.10.2015_31.10.2015.xls')
