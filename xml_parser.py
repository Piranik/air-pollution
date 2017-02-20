import xml.etree.ElementTree as ET
import re

class Xml_Parser(object):
    def __init__(self):
        self.time_pattern = re.compile('(\d{4}\-\d{2})\-(\d{2})T(\d{2}:\d{2}:\d{2}).*')

    def validate_file(self, root):
        valid_date = 'startDate' in root.attrib
        return valid_date

    def parse_file(self, filename):
        measurements = []
        station_info = None
        date = None
        with open(filename, "r") as file:
            tree = ET.parse(file)
            root = tree.getroot()
            if self.validate_file(root):
                date_found = self.time_pattern.match(root.attrib['startDate'])
                date = date_found.group(1)
                station_info = self.parse_station_info(root.find('station'))
                station_info['parameters'] = set()
                for parameter in root.find('station').iter('parameter'):
                    measurements.append(
                        (parameter.attrib, self.parse_param(parameter)))
                    station_info['parameters'].add(parameter.attrib['index'])
        return station_info, date, measurements

    def parse_station_info(self, station_node):
        station_info = station_node.attrib
        station_info['location'] = station_info.pop('description')
        return station_info

    def parse_param(self, parameter_element):
        measurements = []
        for measurement in parameter_element.iter('measurement'):
            measurement_dict = self.parse_param_measurement(measurement)
            measurements.append(measurement_dict)
        return measurements

    def parse_param_measurement(self, measurement_element):
        time_found = self.time_pattern.match(measurement_element.attrib['date'])
        return {'day': time_found.group(2), 'time': time_found.group(3),
                'value': measurement_element.attrib['value']}

if __name__ == '__main__':
    xml_parser = Xml_Parser()
    station_info, date, measurements = xml_parser.parse_file('data_files/RO0076A-DECEMBRIE-2012.xml')
    print station_info, date, measurements

