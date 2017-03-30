from xls_parser import Xls_Parser

class StationsInfoParser(object):

    def __init__(self):
        super(StationsInfoParser, self).__init__()

    def parse_station_file(self, filename):
        xls_parser = Xls_Parser(filename)
        # read header values into the list
        headers = ['', 'code', 'internationalCode', 'zone_code', 'location',
                   'start_date', 'latitude', 'longitude', 'altitude', 'type',
                   'zone_type', 'emission_source', 'address']
        objs = {}
        rows_number, cols_number = xls_parser.get_sheet_dimension()
        for row_index in range(1, rows_number):
            obj = {}
            row = [xls_parser.get_value(row_index, col_index) for col_index in range(cols_number)]
            for i in range(1, cols_number):
                obj[headers[i]] = row[i]
            self.convert_content(obj)
            objs[obj['internationalCode']] = obj
        return objs

    def convert_content(self, obj):
        if obj['location']:
            obj['location'] = obj['location'].lower().strip().replace(' ', '_')
            index_of_line = obj['location'].find('-')
            if index_of_line >= 0:
                obj['location'] = obj['location'][0:index_of_line]

        if obj['address']:
            obj['address'] = obj['address'].lower()

        if obj['type']:
            obj['type'] = obj['type'].lower()

        if obj['emission_source']:
            obj['emission_source'] = obj['emission_source'].lower()


    def parse_distribution_file(self, filename):
        county_stations_organization = {}
        county = None
        county_locality = None
        stations = []
        xls_parser = Xls_Parser(filename, True)

        nr_rows, _ = xls_parser.get_sheet_dimension()

        for row in range(2, nr_rows):
            county_cell_value = str(xls_parser.get_value(row, 0))
            county_locality_cell_value = xls_parser.get_value(row, 1)
            station_international_code = str(xls_parser.get_value(row, 4))
            station_cell_format = xls_parser.get_format_of_cell(row, 4)

            if not county and county_cell_value:
                county = county_cell_value.lower()
            if not county_locality and county_locality_cell_value:
                county_locality = county_locality_cell_value.lower()
            stations.append(station_international_code)

            if station_cell_format.border.bottom_line_style == 2:
                self.add_new_county_entry(county_stations_organization, county,
                                          county_locality, stations)
                county = None
                county_locality = None
                stations = []

        return county_stations_organization

    def add_new_county_entry(self, county_stations_organization, county, county_locality, stations):
        if not county and county_locality:
            county = county_locality
        county = county.strip().lower()
        county_stations_organization[county] = stations

    def parse(self, stations_filename, stations_distribution_filename):
        stations = self.parse_station_file(stations_filename)
        county_stations_organization = self.parse_distribution_file(stations_distribution_filename)
        return stations, county_stations_organization
