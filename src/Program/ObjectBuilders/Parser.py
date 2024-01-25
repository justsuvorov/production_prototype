import pandas as pd
import sqlite3
from Program.Well.MerData import MerData
from abc import ABC
import os
from Program.Production.config_db import CompanyDictionary
#from Program.ObjectBuilders.sql_speaking_objects import GfemSQLSpeakingObject
import datetime
from copy import deepcopy


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



class SetOfWellsParserMonth(Parser):
    def __init__(self,
                 data_path: str,
                 month: str = None,
                 vbd: bool = False
                 ):
        self.__vbd = vbd
        if self.__vbd:
            self.__data_path = data_path + '/VBD.xlsm'
        else:
            self.__data_path = data_path + '/СВОД_NEW_Скв_5лет_испр.xlsm'
        self.__month = pd.to_datetime(month, format='%Y-%m')
        self.__indicator_numbers = [4, 64, 124]
        self.__df = None

    def data(self) -> pd.DataFrame:
        return self.__choose_month()

    def read_excel(self):
        df = pd.read_excel(self.__data_path)
        df.iloc[0,self.__indicator_numbers[0]:self.__indicator_numbers[1]] =  'Oil_' + df.iloc[0, self.__indicator_numbers[0]:self.__indicator_numbers[1]].astype(str)
        df.iloc[0, self.__indicator_numbers[2]:] = 'FCF_'+ df.iloc[0, self.__indicator_numbers[2]:].astype(str)

        df.iloc[0, 0] = 'Месторождение'
        df.iloc[0, 1] = 'Навзание ДНС'
        df.iloc[0, 2] = 'Скважина'
        df.iloc[0, 3] = 'Куст'
        df.columns = df.iloc[0]
        self.__df = df[1:]
       # return df[1:]

    def __choose_month(self):
        if self.__df is None:
            df = self.read_excel()
            print('SetOfWellParser|| Чтение excel')
        else:
            df = self.__df
        new_df = pd.DataFrame()

        new_df['Месторождение'] = df.loc[:,'Месторождение']
        new_df['Скважина'] = df.loc[:,'Скважина']
        new_df['Куст'] = df.loc[:,'Куст']
        new_df['GAP'] = 'No gap'

        new_df['FCF первый месяц:'] = df.loc[:,'FCF_' + str(self.__month)]
        new_df['НДН за первый месяц; тыс. т'] = df.loc[:, 'Oil_' + str(self.__month)]

        return new_df

    def set_month(self, month: str):
        try:
            self.__month = pd.to_datetime(month, format='%Y-%m')
        except:
            print('SetOfWellsParserMonth || Неправильный формат месяца')

class SetOfWellsVBDParserMonth(Parser):
    def __init__(self,
                 data_path: str,
                 month: str = None,

                 ):

        self.__data_path = data_path + '/VBD.xlsm'
        self.__month = pd.to_datetime(month, format='%Y-%m')
        self.__indicator_numbers = [4, 64, 124]
        self.__df = None

    def data(self) -> pd.DataFrame:
        return self.__choose_month()

    def read_excel(self):
        df = pd.read_excel(self.__data_path)
        df.iloc[0,self.__indicator_numbers[0]:self.__indicator_numbers[1]] =  'Oil_' + df.iloc[0, self.__indicator_numbers[0]:self.__indicator_numbers[1]].astype(str)
        df.iloc[0, self.__indicator_numbers[2]:] = 'FCF_'+ df.iloc[0, self.__indicator_numbers[2]:].astype(str)

        df.iloc[0, 0] = 'Месторождение'
        df.iloc[0, 1] = 'Навзание ДНС'
        df.iloc[0, 2] = 'Скважина'
        df.iloc[0, 3] = 'Куст'
        df.columns = df.iloc[0]
        self.__df = df[1:]
       # return df[1:]

    def __choose_month(self):
        if self.__df is None:
            df = self.read_excel()
            print('SetOfWellParser|| Чтение excel')
        else:
            df = self.__df
        new_df = pd.DataFrame()

        new_df['Месторождение'] = df.loc[:,'Месторождение']
        new_df['Скважина'] = df.loc[:,'Скважина']
        new_df['Куст'] = df.loc[:,'Куст']
        new_df['GAP'] = 'No gap'

        new_df['FCF первый месяц:'] = df.loc[:,'FCF_' + str(self.__month)]
        new_df['НДН за первый месяц; тыс. т'] = df.loc[:, 'Oil_'+ str(self.__month)]

        new_df['FCF скользящий год'] = df.loc[:, 'FCF_' + '2023-12-01 00:00:00':'FCF_'  + '2024-12-01 00:00:00'].sum(axis=1)

        new_df['НДН скользящий год'] = df.loc[:, 'Oil_' + '2023-12-01 00:00:00':'Oil_'  + '2024-12-01 00:00:00'].sum(axis=1)

        print(new_df['FCF скользящий год'])
        return new_df

    def set_month(self, month: str):
        try:
            self.__month = pd.to_datetime(month, format='%Y-%m')
        except:
            print('SetOfWellsParserMonth || Неправильный формат месяца')


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


class GfemDatabaseEcmParser(Parser):
    def __init__(self,
                 data_path: str,
                 month: str):
        self.__db_path =  data_path
        self.__month = month
        self.__db = GfemSQLSpeakingObject(path=data_path)


class GfemDataBaseParser(Parser):
    def __init__(self,
                 data_path: str,
                 file_path: str,
                 add_data_from_excel: bool = False,
                 gap: int = 0
                 ):
        self.data_path = data_path
        self.series_names = ['id', 'Тип объекта', 'ДО', 'Месторождение', 'Лицензионный участок',
                             'Объект подготовки', 'Куст', 'Скважина', 'NPV_MAX',	'GAP',
                             'НДН за первый месяц',
                             'FCF первый месяц:', 'НДН за весь период; тыс. т',
                             'НДЖ за весь период; тыс. т', 'FCF за весь период; тыс. руб.',
                             'НДН до ГЭП; тыс. т',
                             'НДЖ до ГЭП; тыс. т',	'FCF до ГЭП; тыс. руб.',
                             'Период расчета; мес.',	'НДН за скользящий год; тыс. т',	'НДЖ за скользящий год; тыс. т',
                             'FCF за скользящий год; тыс. руб.',]
        self.__add_data_from_excel = add_data_from_excel
        self.file_path = file_path
        self.__gap = gap

    def names(self):
        data = sqlite3.connect(self.data_path)
        df = pd.read_sql_query('SELECT * FROM arf_prod_obj_information', data)
        df = df.set_axis(self.series_names, axis=1, )
        df = df.drop(columns=['НДН за первый месяц'])
        pd.set_option('mode.chained_assignment', None)
        df = df.loc[(df['GAP'] > 0)]
        return df[['ДО', 'Месторождение', 'Объект подготовки', 'Куст', 'Скважина']]

    def data(self):
        data = sqlite3.connect(self.data_path)
        df = pd.read_sql_query('SELECT * FROM arf_prod_obj_information', data)
        df = df.set_axis(self.series_names, axis=1, )
        pd.set_option('mode.chained_assignment', None)
        # This code will not complain!

        if self.__add_data_from_excel:
            try:
                add_df = self.__add_query()
                print(add_df.shape[0])
                df1 = df.loc[(df['GAP'] == self.__gap)]
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
                if self.__gap == 0:
                    df1 = df.loc[df['GAP'] == self.__gap]
                    df1.loc[:, 'Статус по рентабельности'] = 'Нерентабельная'
                else:

                    df1 = df.loc[df['GAP'] == 1]
                    df1.loc[:, 'Статус по рентабельности'] = 'ГЭП 1'
                    df2 = df.loc[df['GAP'] == 2]
                    df2.loc[:, 'Статус по рентабельности']= 'ГЭП 2'
                    df1 = pd.concat([df1, df2])

        else:
            df1 = df.loc[df['GAP'] == self.__gap]
            df1.loc[:, 'Статус по рентабельности'] = 'ГЭП ' + str(self.__gap)
        pd.reset_option("mode.chained_assignment")
        df1 = df1.drop(columns=['НДН за первый месяц'])
        return df1

    def __add_query(self):
        try:
            gfem_excel = self.file_path + '\СВОД_Скв_2мес.xlsm'
            add_data = GfemParser(data_path=gfem_excel).add_data()
            print('Файл Excel прочитан. Условно-рентабельных скважин: ', add_data.shape[0])
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
        print('MonitoringActivityParser||Connecting to monitoring db')
        data = sqlite3.connect(self.data_path)

        df = pd.read_sql_query('SELECT * FROM activity_unprofit', data)
    #    self.initial_names = list(df.columns)
        print('MonitoringActivityParser||Data is read')
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
