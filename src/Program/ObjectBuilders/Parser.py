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
        pd.set_option('mode.chained_assignment', None)
        # This code will not complain!

        if self.__add_data_from_excel:
            try:
                add_df = self.__add_query()
                df1 = df.loc[(df['GAP'] == 0)]
                df1.loc[:,'Статус по рентабельности'] = 'Нерентабельная'
                df['temp_name'] = df['Месторождение'] + df['Скважина']
                df1['temp_name'] = df1['Месторождение'] + df1['Скважина']
                df2 = df.loc[df['temp_name'].isin(add_df['id'])]
                df2.loc[:,'Статус по рентабельности'] = 'Рентабельная до первого ремонта'

                df1 = df1.loc[~df1['temp_name'].isin(df2['temp_name'])]
                df1 = pd.concat([df1, df2])
                df1 = df1.drop(columns=['temp_name'])
            except:
                print('Отсутсвуют скважины с ремонтом')
                df1 = df.loc[df['GAP'] == 0]
                df1.loc[:, 'Статус по рентабельности'] = 'Нерентабельная'

        else:
            df1 = df.loc[df['GAP'] == 0]
            df1.loc[:, 'Статус по рентабельности'] = 'Нерентабельная'
        pd.reset_option("mode.chained_assignment")
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
        self.series_names = ['id', 'id_aro',  'Тип объекта', 'Скважина', 'Куст', 'Объект подготовки', 'Месторождение',	'ДО',
                             'Дата внесения', 'Статус по рентабельности', 'Статус по МЭР' ]
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


class MorDBParser(Parser):

    def __init__(self,
                 data_path: str):
        self.data_path = data_path

    def data(self):
        data = sqlite3.connect(self.data_path)
        df = pd.read_sql_query('SELECT * FROM mor_info', data)
        return df
