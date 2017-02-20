from xlrd import open_workbook


class Xls_Parser(object):
	def __init__(self, file_name):
		self.book = open_workbook(file_name)
		self.sheet = self.book.sheet_by_index(0)
		print self.sheet
		# read header values into the list
		self.headers = ['', 'code', 'internationalCode', 'zone_code', 'location', 'start_date', 'latitude', 'longitude', 'altitude', 'type', 'zone_type', 'emission_source', 'address']


	def parse_content(self):
		objects = []
		cols_number = self.sheet.ncols
		for i in range(1, self.sheet.nrows):
			object = {}
			row = [self.sheet.cell(i, col_index).value for col_index in xrange(cols_number)]
			for i in range(1, cols_number):
				object[self.headers[i]] = row[i]
			objects.append(object)
		return objects

	def parse(self):
		objects = self.parse_content()
		return objects


if __name__ == '__main__':
	xls_parser = Xls_Parser('data_files/informatii-privind-statiile-rnmca.xls')
	objects = xls_parser.parse()
	for object in objects:
		print object

	print len(objects)
