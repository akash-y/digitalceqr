from census import Census
import pandas as pd
from us import states

import censusgeocode as cg

import math

from shapely.geometry import Point, Polygon
import geopandas as gpd


class Socio:

    def __init__(self, addr, radius, year, survey, borough, api_key):
        self.addr = addr
        self.radius = radius
        self.county_code = self.init_county_code(borough)
        self.borough = borough

        self.survey = self.init_census_api(survey, year, api_key)

        self.survey_fields_map = self.init_fields_mapper()

    def init_county_code(self, borough):
        if borough == 'Staten Island':
            return '085'
        elif borough == 'Brooklyn':
            return '047'
        elif borough == 'Queens':
            return '081'
        elif borough == 'Manhattan':
            return '061'
        elif borough == 'Bronx':
            return '005'
        else:
            raise Exception("{} is not a valid borough name.".format(borough))

    def init_census_api(self, survey, year, api_key):
        if survey == "acs5":
            return Census(api_key, year=year).acs5
        elif survey == "acs1":
            return Census(api_key, year=year).acs1dp
        elif survey == "census":
            return Census(api_key, year=year).sf1
        else:
            raise Exception("{} is not a valid survey type.".format(survey))

    def init_fields_mapper(self):
        totalHU = 'B25001_001E'
        owner = 'B25003_002E'
        renter = 'B25003_003E'
        population = 'B01003_001E'
        income = 'B19013_001E'
        total_labor = 'B23025_001E'
        unemployed = 'B23025_005E'
        vacancy = 'B25004_001E'

        return {'NAME': 'name',
                population: 'population',
                income: 'income',
                renter: 'renters',
                owner: 'owners',
                totalHU: 'total_housing',
                total_labor: 'total_labor',
                unemployed: 'total_unemployed',
                vacancy: 'vacancy'}

    def get_block_groups_study_area(self):
        addr_census_result = cg.onelineaddress(self.addr)

        # get coordinates of addr
        addr_point = Point(addr_census_result[0]['coordinates']['x'],
                           addr_census_result[0]['coordinates']['y'])

        # get study area pluto data
        study_area = addr_point.buffer(self.radius / 69)
        study_area_polygon = Polygon(study_area.exterior.coords)

        # Load census block groups shape file
        block_groups = gpd.read_file('data/ny_block_groups/tl_2015_36_bg.shp')

        return block_groups[block_groups.apply(lambda row: study_area_polygon.contains(row['geometry'].centroid), axis=1)]

    def get_study_area_data(self):
        column_requests = []
        block_groups_study_area = self.get_block_groups_study_area()

        block_group_study_area_data = []
        for block_group in block_groups_study_area.iterrows():
            bg = block_group[1]
            bg_data = self.survey.state_county_blockgroup(tuple(self.survey_fields_map.keys(
            )), bg['STATEFP'], bg['COUNTYFP'], bg['BLKGRPCE'], bg['TRACTCE'])
            bg_data = bg_data[0]
            bg_data['index'] = bg.name
            block_group_study_area_data.append(bg_data)
        block_group_study_area_data = pd.DataFrame.from_dict(
            block_group_study_area_data)
        block_group_study_area_data.set_index('index')
        return block_group_study_area_data.rename(self.survey_fields_map, axis='columns').dropna()

    def get_borough_data(self):
        borough_data = self.survey.state_county(
            tuple(self.survey_fields_map.keys()), '36', self.county_code)[0]
        borough_data = pd.DataFrame(borough_data, index=[0])
        borough_data = borough_data.rename(
            self.survey_fields_map, axis='columns')
        return borough_data

    def get_borough_summary(self):
        borough_data = self.get_borough_data()
        borough_summary = {}
        borough_summary['population'] = float(borough_data['population'])
        borough_summary['median_income'] = float(borough_data['income'])
        borough_summary['percent_owners'] = float(
            borough_data['owners'] / borough_data['total_housing'] * 100)
        borough_summary['percent_renters'] = float(
            borough_data['renters'] / borough_data['total_housing'] * 100)
        borough_summary['unemployment_rate'] = float(
            borough_data['total_unemployed'] / borough_data['total_labor'] * 100)
        borough_summary['vacancy_rate'] = float(
            borough_data['vacancy'] / borough_data['total_housing'] * 100)
        return borough_summary

    def get_study_area_summary(self):
        study_area_data = self.get_study_area_data()

        # POPULATION
        study_area_summary = {}
        study_area_summary['population'] = study_area_data['population'].sum()

        # MEDIAN INCOME
        weighted_median_income = 0

        for block_group in study_area_data.iterrows():
            bg = block_group[1]
            weighted_median_income += bg['income'] * bg['population']

        study_area_summary['median_income'] = weighted_median_income / \
            study_area_summary['population']

        # PERCENT RENTERS
        study_area_summary['percent_renters'] = study_area_data['renters'].sum(
        ) / study_area_data['total_housing'].sum() * 100
        study_area_summary['percent_owners'] = study_area_data['owners'].sum(
        ) / study_area_data['total_housing'].sum() * 100

        # EMPLOYMENT
        study_area_summary['unemployment_rate'] = study_area_data['total_unemployed'].sum(
        ) / study_area_data['total_labor'].sum() * 100

        # VACANCY
        study_area_summary['vacancy_rate'] = study_area_data['vacancy'].sum(
        ) / study_area_data['total_housing'].sum() * 100
        return study_area_summary

    def get_summary_stats(self):
        study_area_summary = self.get_study_area_summary()
        borough_summary = self.get_borough_summary()
        return pd.DataFrame([borough_summary, study_area_summary], index=[self.borough, 'Study Area'])
