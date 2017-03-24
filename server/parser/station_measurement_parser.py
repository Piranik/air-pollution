from xml_parser import Xml_Parser
import re


_NECESSARY_PARAMS = set([
    'PM10 - aut',
    'Monoxid de azot',
    'Oxizi de azot',
    'Dioxid de sulf',
    'PM10 - grv.',
    'Radiatie solara',
    'Umiditate relativa',
    'Presiune',
    'Temp. 2 m',
    'PM 2.5 - grv.',
    'Viteza vant',
    'Dir. Vant',
    'Precipitatii',
    'Umiditate relativa (int)',
    'Diferenta Umiditate relativa',
    'Ozon',
    'Temp. (int)',
    'Temp. 10m',
    '?T (10m-2m)',
    'PM 2.5 - aut',
    'Oxizi de azot 1'
])

class StationMeasurementParser(object):
    """Parser for xml files that contains measurements for stations"""
    def __init__(self):
        super(StationMeasurementParser, self).__init__()
        self.time_pattern = re.compile('(\d{4}\-\d{2})\-(\d{2})T(\d{2}:\d{2}:\d{2}).*')

    def validate_file(self, root_attributes):
        valid_date = 'startDate' in root_attributes
        return valid_date

    def parse_file(self, filename):
        measurements = []
        station_info = None
        date = None
        xml_parser = Xml_Parser(filename)
        root = xml_parser.get_root()
        root_attributes = xml_parser.get_element_attributes(root)

        if self.validate_file(root_attributes):
            date_match = self.time_pattern.match(root_attributes['startDate'])
            date = date_match.group(1)
            station_node = xml_parser.get_child(root, 'station')
            station_info = self.parse_station_info(station_node)
            station_info['parameters'] = set()
            for parameter in xml_parser.get_childs(station_node, 'parameter'):
                if xml_parser.get_element_attributes(parameter)['name'] in _NECESSARY_PARAMS:
                    measurements.append(
                        (parameter.attrib, self.parse_param(xml_parser, parameter)))
                    parameter_attributes = xml_parser.get_element_attributes(parameter)
                    station_info['parameters'].add(parameter_attributes['index'])
        return station_info, date, measurements

    def parse_station_info(self, station_node):
        station_info = station_node.attrib
        station_info['location'] = station_info.pop('description')
        return station_info

    def parse_param(self, xml_parser, parameter_element):
        measurements = []
        for measurement in xml_parser.get_childs(parameter_element, 'measurement'):
            measurement_dict = self.parse_param_measurement(measurement)
            measurements.append(measurement_dict)
        return measurements

    def parse_param_measurement(self, measurement_element):
        time_found = self.time_pattern.match(measurement_element.attrib['date'])
        return {'day': time_found.group(2), 'time': time_found.group(3),
                'value': measurement_element.attrib['value']}




