from xls_parser import Xls_Parser

START_ROW = 14
OBJECT_PARAMETERS = {'code': 3, 'name': 5, 'type': 6, 'vr': 8,
                     'total_number_cases': 9, 'percentage_of_cases': 10,
                     'acute_casses': 12, 'chronic_cases': 14,
                     'spitalization_total': 16, 'spitalization_acute': 18,
                     'spitalization_chronic': 20, 'dms_acute': 22,
                     'dms_chronic': 23}

class Disease_parser(object):

    def __init__(self, filename):
        super(Disease_parser, self).__init__()
        self.xls_parser = Xls_Parser(filename)

    def parse(self):
        nr_rows, _ = self.xls_parser.get_sheet_dimension()
        disease_objects = []

        for row in range(START_ROW, nr_rows):
            ok_flag, disease_object = self.read_row(row)
            if ok_flag:
                disease_objects.append(disease_object)
        return disease_objects

    def read_value(self, x, y):
        value = self.xls_parser.get_value(x, y)
        if value:
            if type(value).__name__ == 'unicode':
                value = value.replace(u'\xe2', 'a')
                return str(value)
            return value
        return None

    def read_row(self, row_number):
        disease_object = {}
        row_with_data_flag = self.read_value(row_number, OBJECT_PARAMETERS['code'])
        for param in OBJECT_PARAMETERS:
            value = self.read_value(row_number, OBJECT_PARAMETERS[param])
            disease_object[param] = value

        return row_with_data_flag, disease_object

