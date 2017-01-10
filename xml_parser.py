import xml.etree.ElementTree as ET


class Xlm_Parser(object):
	def __init__(self, file_name):
		file = open(file_name, "r")
		tree = ET.parse(file)
		for param in tree.getroot().iter('parameter'):
			print param.attrib
			print param.tag
			print len(param)

		# read header values into the list


	def parse_station_code(self):
		pass

	def get_param_list(self):
		pass

	def parse_param_measurement(self, headers):
		pass

	def parse(self):
		pass

if __name__ == '__main__':
	xls_parser = Xlm_Parser('data_files/RO0076A-DECEMBRIE-2012.xml')
