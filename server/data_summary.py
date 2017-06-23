import xlsxwriter
from managers.resources_manager import Resources_Manager
from managers.statistics_manager import Statistics_Manager


PARAMETERS_POSITION = {}

DISEASE_SUMMARY_HEADERS = ['Disease Code', 'Disease Name', 'Number of Appearances']

MONTHS = ['01', '02', '03', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

YEARS = [2010, 2011, 2012, 2013, 2014, 2015, 2016]


"""
    Write summary to xlsx file.
    Headers
    internation_code
        year
                month
                        param index
"""
def write_summary_for_stations(worksheet, statistics, resource_manager):
    last_row = 0

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
                                        measurements_values[parameter_index])
                last_row += 1
"""
    Create air summary for each county based on air stations inside them.
"""
def create_summary_for_county(county_name, parameters, resources_manager):
    statistics_manager = Statistics_Manager()

    stations = resources_manager.get_stations_by_county(county_name)

    workbook = xlsxwriter.Workbook('summaries/' + county_name + '_summary.xlsx')
    worksheet = workbook.add_worksheet()
    stations_statistics = [statistics_manager.compute_statistics_for_station(station, parameters, resources_manager)
                           for station in stations]
    write_summary_for_stations(worksheet, stations_statistics, resources_manager)

    workbook.close()
    print 'County %s done' % county_name


"""
Create summary for each used air station
"""
def create_summary_for_used_stations(stations, parameters, resources_manager):
    statistics_manager = Statistics_Manager()

    workbook = xlsxwriter.Workbook('summaries/used_stations_summary.xlsx')
    worksheet = workbook.add_worksheet()
    statistics = [statistics_manager.compute_statistics_for_station(station, parameters,
                  resources_manager) for station in stations]

    write_summary_for_stations(worksheet, statistics, resources_manager)

    workbook.close()
    print 'Used stations summary done'
    return statistics

"""
    Create summary for all stations. Not relevant
"""
def create_data_summary():
    res_manager = Resources_Manager()

    counties = [county['name'] for county in res_manager.get_counties()]
    parameters = res_manager.get_all_parameters()

    param_place_index = 4
    for parameter in parameters:
        PARAMETERS_POSITION[parameter['index']] = (param_place_index, parameter['name'])
        param_place_index += 1

    for county in counties:
        create_summary_for_county(county, parameters, res_manager)

"""
Create summary for disease and writes in summaries/diseases_summary.xlsx.
It's used for finding the most frequently diseases.
"""
def create_disease_summary():
    resources_manager = Resources_Manager()
    most_frequently_diseases = []
    for disease in resources_manager.get_all_diseases():
        most_frequently_diseases.append((disease['code'], disease['name'],
                                         len(disease['statistics'])))

    most_frequently_diseases = sorted(most_frequently_diseases, key=lambda d: d[2], reverse=True)
    workbook = xlsxwriter.Workbook('summaries/diseases_summary.xlsx')
    worksheet = workbook.add_worksheet()
    # Headers
    for index, header in enumerate(DISEASE_SUMMARY_HEADERS):
        print index, header
        worksheet.write(0, index, header)

    row = 1;
    for disease in most_frequently_diseases:
        print disease
        worksheet.write(row, 0, disease[0])
        worksheet.write(row, 1, disease[1])
        worksheet.write(row, 2, disease[2])
        row += 1

    workbook.close()



if __name__ == '__main__':
    create_data_summary()
    create_disease_summary()
