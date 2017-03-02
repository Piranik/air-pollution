from xlrd import open_workbook

class Xls_Parser(object):
    def __init__(self, filepath, formatting_info=False):
        super(Xls_Parser, self).__init__()

        print filepath, formatting_info
        self.book = open_workbook(filepath, formatting_info=formatting_info)
        self.sheet = self.book.sheet_by_index(0)

    def get_sheet_dimension(self):
        return self.sheet.nrows, self.sheet.ncols

    def get_cell(self, x, y):
        return self.sheet.cell(x, y)

    def get_value(self, x, y):
        return self.sheet.cell(x, y).value

    def get_format_of_cell(self, x, y):
        xf_index = self.sheet.cell_xf_index(x, y)
        return self.book.xf_list[xf_index]
