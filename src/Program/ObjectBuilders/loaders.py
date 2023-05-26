import pandas as pd
import sqlite3
from abc import ABC



class Loader(ABC):
    def __init__(self,
                 data: pd.DataFrame,
                 source_path: str,
                 ):
        self.data = data
        self.source_path = source_path

    def load_data(self):
        pass


class BlackListLoaderExcel(Loader):
    def __init__(self,
                 data: pd.DataFrame,
                 source_path: str,
                 ):
        super().__init__(data=data,
                         source_path=source_path)

    def load_data(self):
        self.data.to_excel(self.source_path+'\Black_list.xlsx')
        print('Результаты записаны в Excel')


class BlackListLoaderDB(Loader):
    def __init__(self,
                 data: pd.DataFrame,
                 source_path: str,
                 ):
        super().__init__(data=data,
                         source_path=source_path)
        self.initial_names = ['id', 'obj_type', 'well_name', 'well_group_name', 'preparation_obj_name',
                              'field_name', 'company_name', 'date_creation', 'status']

    def load_data(self):

        engine = sqlite3.connect(self.source_path+'\monitoring.db')
        self.data.columns = self.initial_names
        self.data.to_sql('monitoring_unprofit_obj', con=engine, if_exists='replace', index=False)
        print('BlackListLoaderDB||Результаты записаны в Базу данных')


class AROFullLoaderDB(Loader):
    def __init__(self,
                 data: pd.DataFrame,
                 source_path: str,
                 ):
        super().__init__(data=data,
                         source_path=source_path)
        self.initial_names = ['object_id',
                                'npv_max',
                                'fcf_first_month',
                             #   'oil_production_first_month',
                                'oil_production_full',
                                'fluid_extraction_full',
                                'fcf_full',
                                'oil_production_gap',
                                'fluid_extraction_gap',
                                'fcf_gap',
                                'calculation_horizon',
                                'oil_production_year',
                                'fluid_extraction_year',
                                'fcf_year',
                              ]

    def load_data(self):

        self.data.columns = self.initial_names
        engine = sqlite3.connect(self.source_path+'\monitoring.db')
     #   for row in self.data.iterrows():

        self.data.to_sql('monitoring_ecm_prod_full', con=engine, if_exists='replace', index=False)
        print('AROFullLoaderDB||Результаты записаны в Базу данных')


class ActivityLoaderDB(Loader):
    def __init__(self,
                 data: pd.DataFrame,
                 source_path: str,
                 ):
        super().__init__(data=data,
                         source_path=source_path)

    def load_data(self):

        engine = sqlite3.connect(self.source_path+'\monitoring.db')

        self.data.to_sql('activity_unprofit', con=engine, if_exists='replace', index=False)
        print('ActivityLoaderDB||Результаты записаны в Базу данных')


class AROMonthTableLoaderDB(Loader):

    def __init__(self,
                 data: pd.DataFrame,
                 source_path: str,
                 ):
        super().__init__(data=data,
                         source_path=source_path)
