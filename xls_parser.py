from xlrd import open_workbook


class Xls_Parser(object):
	def __init__(self, file_name):
		self.book = open_workbook(file_name)
		self.sheet = self.book.sheet_by_index(0)
		print self.sheet
		# read header values into the list


	def parse_header(self):
		return [self.sheet.cell(0, col_index).value.lower() for col_index in xrange(self.sheet.ncols)]

	def parse_content(self, headers):
		objects = []
		cols_number = self.sheet.ncols
		for i in range(1, self.sheet.nrows):
			object = {}
			row = [self.sheet.cell(i, col_index).value for col_index in xrange(cols_number)]
			for i in range(1, cols_number):
				object[headers[i]] = row[i]
			objects.append(object)
		return objects

	def parse(self):
		headers = self.parse_header()
		objects = self.parse_content(headers)
		return objects


if __name__ == '__main__':
	xls_parser = Xls_Parser('data_files/informatii-privind-statiile-rnmca.xls')
	objects = xls_parser.parse()
	for object in objects:
		print object

	print len(objects)
