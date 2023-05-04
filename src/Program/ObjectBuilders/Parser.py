import pandas as pd
import sqlite3
from Program.Well.MerData import MerData
from abc import ABC


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
        self.series_names = ['id', 'Тип объекта', 'Скважина', 'Куст', 'Объект подготовки', 'Месторождение',	'ДО', 'Дата внесения']
        self.initial_names = None

    def data(self):
        print('Connecting to monitoring db')
        data = sqlite3.connect(self.data_path)

        df = pd.read_sql_query('SELECT * FROM monitoring_unprofit_obj', data)
        self.initial_names = list(df.columns)

        df = df.set_axis(self.series_names, axis=1, )

        return df


class MonitoringFullParser(Parser):
    def __init__(self,
                 data_path: str,
                 ):
        self.data_path = data_path


    def data(self):
        data = sqlite3.connect(self.data_path)

        df = pd.read_sql_query('SELECT * FROM monitoring_ecm_prod_full', data)

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
                              'field_name', 'company_name', 'date_creation']

    def load_data(self):

        engine = sqlite3.connect(self.source_path+'\monitoring.db')
        self.data.columns = self.initial_names
        self.data.to_sql('monitoring_unprofit_obj', con=engine, if_exists='replace', index=False)
        print('Результаты записаны в Базу данных')


