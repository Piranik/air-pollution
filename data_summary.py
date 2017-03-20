import xlsxwriter
from managers.resources_manager import Resources_Manager
from managers.controllers.database_controller import Database_Controller


PARAMETERS_POSITION = {}

MONTHS = ['01', '02', '03', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

YEARS = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]


def compute_average(measurements):
    if measurements:
        measurements_sum = 0
        for measurement in measurements:
            measurements_sum += float(measurement['value'])

        return float(measurements_sum) / len(measurements)
    return 0


def write_summary_for_stations(worksheet, stations, parameters, resource_manager):
    last_row = 0
    for station in stations:
        # Headers
        worksheet.write(last_row, 0, station['internationalCode'])
        worksheet.write(last_row+1, 0, station['county'])
        param_place_index = 4
        for parameter in parameters:
            worksheet.write(last_row, param_place_index, parameter['name'])
            PARAMETERS_POSITION[parameter['index']] = param_place_index
            param_place_index += 1
        last_row += 2

        for year in YEARS:
            worksheet.write(last_row, 1, year)
            last_row += 1
            for month in MONTHS:
                worksheet.write(last_row, 2, month)
                measurements = resource_manager.get_measurements_for_station(
                    station['internationalCode'], year, month)
                for measurement in measurements:
                    if measurement['parameter_index'] in PARAMETERS_POSITION:
                        worksheet.write(last_row,
                                        PARAMETERS_POSITION[measurement['parameter_index']],
                                        compute_average(measurement['measurements']))
                last_row += 1


def create_summary_for_county(county_name, parameters, resources_manager):
    stations = resources_manager.get_stations_by_county(county_name)

    workbook = xlsxwriter.Workbook('summaries/' + county_name + '_summary.xlsx')
    worksheet = workbook.add_worksheet()

    write_summary_for_stations(worksheet, stations, parameters, resources_manager)

    workbook.close()
    print 'County %s done' % county_name


def create_summary_for_used_stations(stations, parameters, resources_manager):
    workbook = xlsxwriter.Workbook('summaries/used_stations_summary.xlsx')
    worksheet = workbook.add_worksheet()

    write_summary_for_stations(worksheet, stations, parameters, resources_manager)

    workbook.close()
    print 'Used stations summary done'


def create_data_summary():
    db_controller = Database_Controller()
    res_manager = Resources_Manager(db_controller)

    counties = [county['name'] for county in res_manager.get_counties()]
    parameters = res_manager.get_all_parameters()

    for county in counties:
        create_summary_for_county(county, parameters, res_manager)

if __name__ == '__main__':
    create_data_summary()
