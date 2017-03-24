from config_utils.config import ConfigYaml
from managers.resources_manager import Resources_Manager


_START_YEAR = 2010
_LAST_YEAR = 2017

class Statistics_Manager(object):
    """Statistics Manager for Stations"""

    def __init__(self):
        super(Statistics_Manager, self).__init__()
        self.resources_manager = Resources_Manager()
        self.counties = self.resources_manager.get_counties()

    def compute_element_index_codification(self, elements):
        elements_indexes = {}
        index = 0
        for element in elements:
            elements_indexes[element] = index
            index += 1
        return elements_indexes

    def air_pollution_county_statistics(self):
        """Return statistics between air_pollution and counties.

        Returns:
            statistics: 4-dimensional matrix. stastics[county][year][month][parameter] = value

        """

        counties = [x['name'] for x in self.resources_manager.get_counties()]
        counties = sorted(counties)

        parameters = [x['index'] for x in self.resources_manager.get_used_parameters()]
        parameters = sorted(parameters)

        counties_indexes = self.compute_element_index_codification(counties)
        parameter_indexes = self.compute_element_index_codification(parameters)

        stations_statistics = self.resources_manager.get_stations_statistics()

        statistics = [[[[0 for _ in parameters] for _ in range(12)] for _ in range(2010, 2017)]
                      for _ in counties]

        stations_in_counties = [set() for county in counties]

        # Create 4d matrix of statistics for each county
        for station in stations_statistics:
            county_index = counties_indexes[station['county']]
            stations_in_counties[county_index].add(station['internationalCode'])
            for statistic in station['statistics']:
                statistic_year = int(statistic['year'])
                if statistic_year >= _START_YEAR:
                    year_index = statistic_year - _START_YEAR
                    month = int(statistic['month']) - 1
                    for parameter in statistic['values']:
                        parameter_index = parameter_indexes[int(parameter)]
                        statistics[county_index][year_index][month][parameter_index] += statistic['values'][parameter]

        for county in counties:
            county_index = counties_indexes[county]
            stations_no = len(stations_in_counties[county_index])
            if stations_no > 1:
                for year_index in range(_LAST_YEAR - _START_YEAR):
                    for month_index in range(12):
                        for param_index in range(len(parameters)):
                            statistics[county_index][year_index][month_index][param_index] /= stations_no

        return stations_in_counties, statistics

    def disease_county_statistics(self):
        """Return statistics between diseases and counties.

        Returns:
            statistics: 3-dimensional matrix. statistics[county][year][month] = value

        """
        pass


