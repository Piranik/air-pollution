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


def compute_statistics_for_station(station, parameters, resources_manager):
    station_statistics = {}
    station_statistics['internationalCode'] = station['internationalCode']
    station_statistics['county'] = station['county']
    statistics = []
    for year in YEARS:
        for month in MONTHS:
            parameter_value_dict = {}
            for parameter in parameters:
                measurements = resources_manager.get_measurements_for_station(
                    station['internationalCode'], year, month, parameter['index'])
                if measurements:
                    parameter_value_dict[str(parameter['index'])] = compute_average(
                        measurements[0]['measurements'])
            statistics.append({'year': year, 'month': month, 'values': parameter_value_dict})

    station_statistics['statistics'] = statistics
    return station_statistics


def write_summary_for_stations(worksheet, statistics, parameters, resource_manager):
    last_row = 0

    param_place_index = 4
    for parameter in parameters:
        # worksheet.write(last_row, param_place_index, parameter['name'])
        PARAMETERS_POSITION[parameter['index']] = (param_place_index, parameter['name'])
        param_place_index += 1

    for station_statistics in statistics:
        # Headers
        worksheet.write(last_row, 0, station_statistics['internationalCode'])
        # worksheet.write(last_row+1, 0, station_statistics['county'])

        last_row += 1
        for parameter_index in PARAMETERS_POSITION:
            parameter_position, parameter_name = PARAMETERS_POSITION[parameter_index]
            worksheet.write(last_row, parameter_position, parameter_name)

        for year in YEARS:
            worksheet.write(last_row, 1, year)
            last_row += 1
            year_statistics = [x for x in station_statistics['statistics'] if x['year'] == year]

            for month in MONTHS:
                worksheet.write(last_row, 2, month)
                measurements_values = [x['values'] for x in year_statistics if x['month'] ==
                                       month][0]

                for parameter_index in measurements_values:
                    if parameter_index in PARAMETERS_POSITION:
                        parameter_position, _ = PARAMETERS_POSITION[parameter_index]
                        worksheet.write(last_row, parameter_position,
                                        measurements_values[str(parameter_index)])
                last_row += 1


def create_summary_for_county(county_name, parameters, resources_manager):
    stations = resources_manager.get_stations_by_county(county_name)

    workbook = xlsxwriter.Workbook('summaries/' + county_name + '_summary.xlsx')
    worksheet = workbook.add_worksheet()
    stations_statistics = [compute_statistics_for_station(station, parameters, resources_manager)
                           for station in stations]
    write_summary_for_stations(worksheet, stations_statistics, parameters, resources_manager)

    workbook.close()
    print 'County %s done' % county_name


def create_summary_for_used_stations(stations, parameters, resources_manager):
    print parameters
    workbook = xlsxwriter.Workbook('summaries/used_stations_summary.xlsx')
    worksheet = workbook.add_worksheet()
    statistics = [compute_statistics_for_station(station, parameters, resources_manager)
                  for station in stations]

    write_summary_for_stations(worksheet, statistics, parameters, resources_manager)

    workbook.close()
    print 'Used stations summary done'
    return statistics


def create_data_summary():
    db_controller = Database_Controller()
    res_manager = Resources_Manager(db_controller)

    counties = [county['name'] for county in res_manager.get_counties()]
    parameters = res_manager.get_all_parameters()

    for county in counties:
        create_summary_for_county(county, parameters, res_manager)

if __name__ == '__main__':
    create_data_summary()
