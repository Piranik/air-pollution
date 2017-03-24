import xml.etree.ElementTree as ET

class Xml_Parser(object):
    def __init__(self, filename):
        self.filename = filename
        self.parser = None
        self.tree = None
        self.open_file()

    def open_file(self):
        with open(self.filename, "r") as station_file:
            parser = ET.XMLParser(encoding='utf-8')
            self.tree = ET.parse(station_file, parser)

    def get_root(self):
        return self.tree.getroot()

    def get_child(self, element, child_name):
        return element.find(child_name)

    def get_childs(self, element, child_name):
        return element.iter(child_name)

    def get_element_attributes(self, element):
        return element.attrib

if __name__ == '__main__':
    xml_parser = Xml_Parser('datasets_all/resource157.xml')
    root = xml_parser.get_root()
    print root
    station = xml_parser.get_child(root, 'station')
    print station
    parameters = xml_parser.get_childs(station, 'parameter')
    print parameters

