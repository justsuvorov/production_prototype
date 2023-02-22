import pandas as pd
from abc import ABC
from Program.Production.InputParameters import *
from pathlib import Path
import os
import datetime as dt

class GUIInterface(ABC):
    def __init__(self):
        pass

    def parameter_of_algorithm(self) -> ParametersOfAlgorithm:
        pass

    def time_parameters(self) -> TimeParameters:
        pass


class ExcelInterface(GUIInterface):
    def __init__(self,
                 filepath: Path):
        self.filepath = filepath

    def parameter_of_algorithm(self) -> ParametersOfAlgorithm:
        df = self.__data()

        time_lag_step = df['Исходные данные'].loc['Количество дней на включение']
        compensation = df['Исходные данные'].loc['Полная компенсация накопленной добычи']
        cluster_min_liquid = self.__clusters(df=df)
        crew_constraints = self.__crew(df=df)

        return ParametersOfAlgorithm(
                                    value=8000,
                                    time_lag_step=time_lag_step,
                                    max_objects_per_day=crew_constraints['max_objects_per_day'],
                                    days_per_object=crew_constraints['days_per_object'],
                                    cluster_min_liquid=cluster_min_liquid,
                                    compensation=compensation,
                                    crew_constraints=crew_constraints
                                    )

    def time_parameters(self) -> TimeParameters:
        df = self.__data()
        time_step = 'Day'
        date_start = pd.to_datetime(df['Исходные данные'].loc['Текущая дата']).date()
        date_begin = pd.to_datetime(df['Исходные данные'].loc['Начало периода']).date()
        date_end = pd.to_datetime(df['Исходные данные'].loc['Конец периода']).date()
        return TimeParameters(
                             date_end=date_end,
                             date_begin=date_begin,
                             time_step=time_step,
                             current_date=date_start,
                             )

    def __data(self):
        """ Входные параметры из Excel"""
        DATA = self.filepath / 'Балансировка компенсационных мероприятий для НРФ.xlsm'
        df = pd.read_excel(DATA, sheet_name='Исходные данные', index_col=0)
        return df

    def find_gap(self):
        if os.path.exists(self.filepath / 'СВОД_Скв_NGT.xlsm'):
            find_gap = False
        else:
            find_gap = True
        return find_gap

    def __clusters(self, df):
        if df['Исходные данные'].loc['Учет ограничений по ДНС']:
            try:
                cluster_min_liquid = pd.read_excel(self.filepath / 'Ограничения.xlsx',
                                                   sheet_name='Минимальный Qж на ДНС', index_col=0)
                print('Файл с ограничениями прочитан.')
            except FileNotFoundError:
                print('Нет файла с ограничениями по ДНС.')
                cluster_min_liquid = 0

            except ValueError:
                print('Ошибка в чтении файла ограничений. Ограничения отключены')
                cluster_min_liquid = 0
        else:
            cluster_min_liquid = 0
        return cluster_min_liquid

    def __crew(self, df):
        constraints_from_file = False
        max_objects_per_day = df['Исходные данные'].loc['Максимальное количество бригад']
        days_per_object = df['Исходные данные'].loc['Количество дней на включение']
        crew_constraints = {'Constraints': "No constraint"}
        if df['Исходные данные'].loc['Учет ограничений по бригадам из файла']:
            try:
                data = pd.read_excel(self.filepath / 'Ограничения.xlsx',
                                                   sheet_name='Ограничения по бригадам', index_col=0)
                print('Файл с ограничениями прочитан.')
                crew_constraints['Кол-во бригад'] = data['Кол-во бригад'].to_dict()
                max_objects_per_day = data['Кол-во бригад'].sum()
                days_per_object = df['Исходные данные'].loc['Количество дней на включение']
                constraints_from_file = True

            except FileNotFoundError:
                print('Нет файла с ограничениями по ДНС. Приняты общие значения без привязки к месторождениям')

            except ValueError:
                print('Ошибка в чтении файла ограничений. Приняты общие значения без привязки к месторождениям')

        return {'max_objects_per_day': max_objects_per_day, 'days_per_object': days_per_object,
                'crew_constraints': crew_constraints, 'constraints_from_file': constraints_from_file}

    def chosen_objects(self):
        df = self.__data()
        try:
            company = df['Исходные данные'].loc['Выбор ДО']
            field1 = df['Исходные данные'].loc['Месторождение']
            if field1 == 'Все месторождения':
                field = self.__field_names(df=df, company=company)
            else:
                field = [field1]
        except:
            company = 'All'
            field = 'All'
        finally:
            return company, field

    def __field_names(self, df, company):
        DATA = self.filepath / 'Балансировка компенсационных мероприятий для НРФ.xlsm'
        df2 = pd.read_excel(DATA, sheet_name='Словарь ДО')
        df3 = df2[company].loc[2:29].dropna()

        return df3.values.tolist()
