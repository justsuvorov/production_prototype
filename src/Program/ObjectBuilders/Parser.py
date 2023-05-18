import pandas as pd
import sqlite3
from Program.Well.MerData import MerData
from abc import ABC
import os
from Program.Production.config_db import CompanyDictionary


# from MerData import MerData
#from ObjectStatus import ObjectStatus

class Parser:

    def data(self) :#-> pd.DataFrame:
        pass

    def gtm_object(self):
        pass

    def domain_model(self):
        pass


class MerParser(Parser):
    def __init__(self,
                 merData: MerData
                 ):
        self.merData = merData

    def data(self) :#-> pd.DataFrame:
        data = self._mer()[0]
        return data

    def _mer(self):
        return self.merData.dataframe()


class SetOfWellsParser(Parser):
    def __init__(self,
                 data_path: str,
                 ):
        self.data_path = data_path

    def data(self) -> pd.DataFrame:
        return pd.read_excel(self.data_path).loc[1:]


class GfemParser(Parser):
    def __init__(self,
                 data_path: str,
                 ):
        self.data_path = data_path

    def data(self) -> pd.DataFrame:
        return pd.read_excel(self.data_path,)[['Месторождение','Скважина', 'Куст', 'GAP', 'FCF первый месяц:','НДН за первый месяц; тыс. т']]

    def aro_data(self) -> pd.DataFrame:
        df = pd.read_excel(self.data_path )
        df = df.loc[df['GAP'] == 0]
        return df

    def add_data(self) -> pd.DataFrame:
        df = pd.read_excel(self.data_path)[['id',
            'Месторождение',
            'Куст', 'Скважина', 'GAP',
            ]

        ]
        df = df.loc[df['GAP'] == 1]
        return df


class PortuResultsParser(Parser):
    def __init__(self,
                 data_path: str,
                 ):
        self.data_path = data_path

    def data(self):
        return pd.read_excel(self.data_path, None)


class GfemDataBaseParser(Parser):
    def __init__(self,
                 data_path: str,
                 file_path: str,
                 add_data_from_excel: bool = False,
                 ):
        self.data_path = data_path
        self.series_names = ['id', 'Тип объекта', 'ДО', 'Месторождение', 'Лицензионный участок',
                             'Объект подготовки', 'Куст', 'Скважина', 'NPV_MAX',	'GAP',
                             'FCF первый месяц:', 'НДН за весь период; тыс. т',
                             'НДЖ за весь период; тыс. т', 'FCF за весь период; тыс. руб.',
                             'НДН до ГЭП; тыс. т',
                             'НДЖ до ГЭП; тыс. т',	'FCF до ГЭП; тыс. руб.',
                             'Период расчета; мес.',	'НДН за скользящий год; тыс. т',	'НДЖ за скользящий год; тыс. т',
                             'FCF за скользящий год; тыс. руб.',]
        self.__add_data_from_excel = add_data_from_excel
        self.file_path = file_path

    def data(self):
        data = sqlite3.connect(self.data_path)
        df = pd.read_sql_query('SELECT * FROM arf_prod_obj_information', data)
        df = df.set_axis(self.series_names, axis=1, )
        if self.__add_data_from_excel:
            add_df = self.__add_query()
            df1 = df.loc[(df['GAP'] == 0)]
            df1['Статус по рентабельности'] = 'Нерентабельная'
            df['temp_name'] = df['Месторождение'] + df['Скважина']
            df2 = df.loc[df['temp_name'].isin(add_df['id'])]
            df2['Статус по рентабельности'] = 'Рентабельная до первого ремонта'
            df1 = pd.concat([df1, df2])
            df1 = df1.drop(columns=['temp_name'])

        else:
            df1 = df.loc[df['GAP'] == 0]
            df1['Статус по рентабельности'] = 'Нерентабельная'

        return df1

    def __add_query(self):
        try:
            gfem_excel = self.file_path + '\СВОД_Скв_2мес.xlsm'
            add_data = GfemParser(data_path=gfem_excel).add_data()
            print('Файл Excel прочитан')
            add_data['Статус по рентабельности'] = 'Рентабельная до первого ремонта'

        except:
            print('Отсутствует файл excel или неправильное название')
            add_data = pd.DataFrame(columns=self.series_names)
        return add_data

    def transfer_month_table(self, path: str):

        data = sqlite3.connect(self.data_path)
        curs = data.cursor()
        mdb_path = path + '\monitoring.db'
        curs.execute('ATTACH "' + mdb_path + '" AS m')
        curs.execute(
            '''INSERT OR IGNORE INTO m.monitoring_ecm_prod_monthly SELECT * FROM arf_prod_ecm WHERE id_parent in (SELECT object_id FROM m.monitoring_ecm_prod_full)'''
            )

        data.commit()

        data.close()


    def merge_prep_objects(self, path: str):
        data = sqlite3.connect(self.data_path)
        curs = data.cursor()
        mdb_path = path + '\monitoring.db'

        curs.execute('ATTACH "' + mdb_path + '" AS m')
        #    curs.execute('''INSERT OR IGNORE INTO m.monitoring_ecm_prod_monthly SELECT * FROM arf_prod_ecm WHERE id_parent in (SELECT id FROM arf_prod_obj_information WHERE gap_period = 0)'''
        curs.execute(
            '''INSERT OR IGNORE INTO m.monitoring_ecm_prod_monthly SELECT * FROM arf_prod_ecm WHERE id_parent in (SELECT object_id FROM m.monitoring_ecm_prod_full)'''

        )

        data.commit()

        data.close()


class GfemMonthDataParser(Parser):
    def __init__(self,
                 data_path: str,
                 ):
        self.data_path = data_path
        """
        self.series_names = ['id', 'Тип объекта', 'ДО', 'Месторождение', 'Лицензионный участок',
                             'Объект подготовки', 'Куст', 'Скважина', 'NPV_MAX',	'GAP',
                             'FCF первый месяц:', 'НДН за весь период; тыс. т',
                             'НДЖ за весь период; тыс. т', 'FCF за весь период; тыс. руб.',
                             'НДН до ГЭП; тыс. т',
                             'НДЖ до ГЭП; тыс. т',	'FCF до ГЭП; тыс. руб.',
                             'Период расчета; мес.',	'НДН за скользящий год; тыс. т',	'НДЖ за скользящий год; тыс. т',
                             'FCF за скользящий год; тыс. руб.',]
        """
    def data(self):
        data = sqlite3.connect(self.data_path)
        df = pd.read_sql_query('SELECT * FROM arf_prod_obj_information', data)
        df = df.set_axis(self.series_names, axis=1, )
        df = df.loc[df['GAP'] == 0]

        return df


class MonitoringBaseParser(Parser):
    def __init__(self,
                 data_path: str,
                 ):
        self.data_path = data_path
        self.series_names = ['id', 'Тип объекта', 'Скважина', 'Куст', 'Объект подготовки', 'Месторождение',	'ДО', 'Дата внесения', 'Статус']
        self.initial_names = None

    def data(self):
        print('MonitoringBaseParser||Connecting to monitoring db')
        data = sqlite3.connect(self.data_path)

        df = pd.read_sql_query('SELECT * FROM monitoring_unprofit_obj', data)
        self.initial_names = list(df.columns)

        df = df.set_axis(self.series_names, axis=1, )
        print('Data is read')
        return df


class MonitoringFullParser(Parser):
    def __init__(self,
                 data_path: str,
                 ):
        self.data_path = data_path


    def data(self):
        print('MonitoringFullParser||Connecting to monitoring db')
        data = sqlite3.connect(self.data_path)

        df = pd.read_sql_query('SELECT * FROM monitoring_ecm_prod_full', data)
        print('MonitoringFullParser||Data is read')
        return df


class MonitoringActivityParser(Parser):
    def __init__(self,
                 data_path: str):
        self.data_path = data_path
    #  self.series_names = ['id объекта', 'ДО','Месторождение', 'Скважина', 'Куст', 'ДНС', 	'ДО', 'Дата внесения', 'Статус']
        self.initial_names = None

    def data(self):
        print('MonitoringFullParser||Connecting to monitoring db')
        data = sqlite3.connect(self.data_path)

        df = pd.read_sql_query('SELECT * FROM activity_unprofit', data)
    #    self.initial_names = list(df.columns)
        print('MonitoringFullParser||Data is read')
       # df = df.set_axis(self.series_names, axis=1, )

        return df

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
        self.initial_names = ['object_id', 'activity_id', 'activity_comment', 'date_planning', 'date_fact',
                              'responsible_person', 'obj_status', 'date_creation', ]

    def load_data(self):

        engine = sqlite3.connect(self.source_path+'\monitoring.db')
        self.data.columns = self.initial_names
        self.data.to_sql('activity_unprofit', con=engine, if_exists='replace', index=False)
        print('ActivityLoaderDB||Результаты записаны в Базу данных')


class AROMonthTableLoaderDB(Loader):

    def __init__(self,
                 data: pd.DataFrame,
                 source_path: str,
                 ):
        super().__init__(data=data,
                         source_path=source_path)


class SQLSpeakingObject:
    def __init__(self,
                 db_name: str,
                ):
        self.db_name = db_name
        self.cursor = None
        try:
            connection = sqlite3.connect(self.db_name)
            self.cursor = connection.cursor()
            print('Connected to ', db_name)
          #  connection.close()
        except:
            print('Unable to connect to db', self.db_name)


class GfemSQLSpeakingObject(SQLSpeakingObject):
    def __init__(self,
                 path: str,
                 ):
        self.path = path
        super(GfemSQLSpeakingObject, self).__init__(db_name=self.path+'\gfem_results.db',
                                                    )
            
#    def


class MonitoringSQLSpeakingObject(SQLSpeakingObject):
    def __init__(self,
                 path: str,):
        self.path = path
        self.db_name = self.path + '\monitoring.db'
        super().__init__(db_name=self.db_name)

        self.__monitoring_base_parser = MonitoringBaseParser(data_path=self.db_name )
        self.__monitoring_full_parser = MonitoringFullParser(data_path=self.db_name )
        self.__monitoring_activity_parser = MonitoringActivityParser(data_path=self.db_name )

    def black_list_from_db(self):
        return self.__monitoring_base_parser.data()

    def full_data_black_list_from_db(self):
        return self.__monitoring_full_parser.data()

    def activity_data_from_db(self):
        return self.__monitoring_activity_parser.data()

    def load_activity_data_to_db(self, data):
        ActivityLoaderDB(data=data, source_path=self.path).load_data()

    def load_black_list_to_db(self, data: pd.DataFrame):
        BlackListLoaderDB(data=data, source_path=self.path).load_data()

    def load_full_data_to_db(self, data: pd.DataFrame):
        AROFullLoaderDB(data=data, source_path=self.path).load_data()

    def insert(self):
        if self.df is None:
            print('No data to insert')
        else:
            for raw in self.df.iterrows():
                self.cursor.execute('''INSERT OR IGNORE''')