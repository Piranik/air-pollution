import xlsxwriter
from database_controller import Database_Controller
from resources_manager import Resources_Manager


def create_data_summary():
    MONTHS = ['01', '02', '03', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    YEARS = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
    db_controller = Database_Controller()
    res_manager = Resources_Manager(db_controller)

    workbook = xlsxwriter.Workbook('data_summary.xlsx')
    worksheet = workbook.add_worksheet()

    row = col = 0

    empty_stations = set()

    # write headers
    worksheet.write(row, col, 'COLECTII GOALE')
    row += 1

    stations = res_manager.get_stations()

    print 'Checking empty collectons'
    for station in stations:
        measurements = res_manager.get_measurements_for_station(station['internationalCode'])
        if not measurements:
            empty_stations.add(station['internationalCode'])
            worksheet.write(row, col, station['internationalCode'])
            col += 1

    row += 1
    col = 0
    print 'Done'
    # write headers
    worksheet.write(row, col, 'STATIE')
    worksheet.write(row, col+1, 'AN')
    worksheet.write(row, col+2, 'LUNA')
    worksheet.write(row, col+3, 'PARAMAETRU')
    worksheet.write(row, col+4, 'NR_MASURATORI')

    print 'Writing Summary for stations'
    row += 1
    for station in stations:
        print 'Station %s' % station['internationalCode']
        if (empty_stations and station not in empty_stations) or not empty_stations:
            col = 0
            worksheet.write(row, col, station['internationalCode'])
            for year in YEARS:
                col = 1
                worksheet.write(row, col, year)
                for month in MONTHS:
                    col = 2
                    worksheet.write(row, col, month)
                    for parameter_index in station['parameters']:
                        col = 3
                        parameter = res_manager.get_parameter(parameter_index)
                        measurements = res_manager.get_measurements_for_station(station['internationalCode'], year, month, parameter_index)
                        worksheet.write(row, col, parameter['name'])
                        if measurements:
                            worksheet.write(row, col+1, len(measurements[0]['measurements']))
                        else:
                            worksheet.write(row, col+1, 'Not exists')
                        row += 1
        print 'Station %s done' % station['internationalCode']

    workbook.close()

if __name__ == '__main__':
    create_data_summary()
