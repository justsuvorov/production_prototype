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
        max_objects_per_day = df['Исходные данные'].loc['Максимальное количество бригад']
        days_per_object = df['Исходные данные'].loc['Количество дней на включение']
        compensation = df['Исходные данные'].loc['Полная компенсация накопленной добычи']
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
        return ParametersOfAlgorithm(
                                    value=8000,
                                    time_lag_step=time_lag_step,
                                    max_objects_per_day=max_objects_per_day,
                                    days_per_object=days_per_object,
                                    cluster_min_liquid=cluster_min_liquid,
                                    compensation=compensation,
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
