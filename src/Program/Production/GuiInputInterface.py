import pandas as pd
from abc import ABC
from Program.Production.InputParameters import *
from pathlib import Path
import os
import datetime as dt
import edifice

class GUIInterface(ABC):
    """
    Абстрактный класс графического интерфейса.

    :returns
    parameter_of_algorithm:
    time_parameters
    """
    def __init__(self):
        pass

    def parameter_of_algorithm(self) -> ParametersOfAlgorithm:
        pass

    def time_parameters(self) -> TimeParameters:
        pass


class ExcelInterface(GUIInterface):
    """
    класс графического интерфейса Excel. Считывает данные с листа "Исходные данные" и "Словарь ДО". Формирует
    обекты классов исходных данных для балансировщика

    inputs:
    filepath: путь к файлу Excel

    :returns
    parameter_of_algorithm:
    time_parameters
    company_iterations: количество расчетов балансировки (ДО)
    field_iterations: количество расчетов балансировки по месторождениям для выбранного ДО
    chosen_objects: формирует фильтра для PreparedDomainModel
    qlik: булева переменная для использования QlikExcelResult

    """
    def __init__(self,
                 filepath: Path,
                 ):
        self.filepath = filepath
        self.companies_names = None
        self.fields_names = None


    def parameter_of_algorithm(self, company_index: int = None, field_index: int = None) -> ParametersOfAlgorithm:
        df = self.__data()
        all_companies_option, all_fields_option = self.calculation_parameters()
        if (company_index is None) and (field_index is None) or not (all_companies_option or all_fields_option):
            time_lag_step = df['Исходные данные'].loc['Количество дней на включение']
            compensation = df['Исходные данные'].loc['Полная компенсация накопленной добычи']
            cluster_min_liquid = self.__clusters(df=df)
            crew_constraints = self.__crew(df=df)

        else:
            DATA = self.filepath / 'Балансировка компенсационных мероприятий для НРФ.xlsm'
            df2 = pd.read_excel(DATA, sheet_name='Словарь ДО')
           # i = df2.columns.get_loc(key=self.companies_names[company_index])
            df3 = df2.loc[df2['Список ДО'] == self.companies_names[company_index]]
            df3 = df3.loc[df2['Месторождение'] == self.fields_names[field_index]]
            time_lag_step = df3['ВНР, суток'].iloc[0]
            max_objects_per_day = df3['Количество бригад'].iloc[0]
            constraints_from_file = False
            days_per_object = df3['Время ремонта, суток'].iloc[0]
            cluster_min_liquid = self.__clusters(df=df)
            compensation = df['Исходные данные'].loc['Полная компенсация накопленной добычи']
            crew = {'Constraints': "No constraint"}
            crew_constraints = {'max_objects_per_day': max_objects_per_day, 'days_per_object': days_per_object,
                                'crew_constraints': crew, 'constraints_from_file': constraints_from_file}

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

    def chosen_objects(self, company_index: int = 0, field_index: int = 0):
        df = self.__data()
        all_companies_option, all_fields_option = self.calculation_parameters()
        try:
            if (not all_companies_option) and (not all_fields_option):
                company = df['Исходные данные'].loc['Выбор ДО']
                self.companies_names = company
                field1 = df['Исходные данные'].loc['Месторождение']
                self.fields_names = field1
                if field1 == 'Все месторождения':
                    field = self.__field_names(company=company)
                else:
                    field = [field1]
            elif all_companies_option and (not all_fields_option):
                company = self.companies_names[company_index]
                field = self.__field_names(company=company)

            elif (not all_companies_option) and all_fields_option:
                company = df['Исходные данные'].loc['Выбор ДО']
                field = self.__field_names(company=company)[field_index]
                if isinstance(field, str):
                    field = [field]
            elif all_companies_option and all_fields_option:
                company = self.companies_names[company_index]
                field = self.__field_names(company=company)[field_index]
                if isinstance(field, str):
                    field = [field]

        except:
            company = 'All'
            field = 'All'
            print('Расчет для всех исходных данных без фильтра')
        finally:
            return {'company': company, 'field': field}

    def __field_names(self, company):
        DATA = self.filepath / 'Балансировка компенсационных мероприятий для НРФ.xlsm'
        df2 = pd.read_excel(DATA, sheet_name='Словарь ДО')
        df3 = df2.loc[df2['Список ДО'] == company]
        field_names = df3['Месторождение'].iloc[1:].values.tolist()
        return field_names

    def calculation_parameters(self,):
        df = self.__data()
        all_companies_option = df['Исходные данные'].loc['Расчет всех ДО']
        all_fields_option = df['Исходные данные'].loc['Расчет всех месторождений']
        return bool(all_companies_option), bool(all_fields_option)

    def company_iterations(self):
        iterations = 1
        all_companies_option, all_fields_option = self.calculation_parameters()
        DATA = self.filepath / 'Балансировка компенсационных мероприятий для НРФ.xlsm'

        if all_companies_option:
            df = pd.read_excel(DATA, sheet_name='Словарь ДО')
            self.companies_names = df['ДО'].loc[:15].dropna().to_list()
            iterations += len(self.companies_names) - 1
        else:
            df = self.__data()
            company = df['Исходные данные'].loc['Выбор ДО']
            self.companies_names = [company]

        return iterations

    def field_iterations(self, company_index: int):
        iterations = 1
        all_companies_option, all_fields_option = self.calculation_parameters()
        if all_fields_option:

            self.fields_names = self.__field_names(company=self.companies_names[company_index])
            iterations = len(self.fields_names)
        else:
            df = self.__data()
            field = df['Исходные данные'].loc['Месторождение']
            self.fields_names = [field]

        return iterations

    def qlik(self) -> bool:
        df = self.__data()
        try:
            export = df['Исходные данные'].loc['Экспорт для Qlik']
        except:
            export = True
        return export

class TodoApp(edifice.Component):
    def __init__(self):
        super().__init__()
        self.items = []
        self.text = ""

    def render(self):
        return View(style={"margin": 10})(
            Label("TODO"),
            TodoList(items=self.items),
            View(layout="row")(
                Label("What needs to be done?"),
                TextInput(self.text,
                          on_change=lambda text:self.set_state(text=text)),
                Button(f"Add #{len(self.items)+1}",
                       on_click=self.add_item)
            )
        )

    def add_item(self, e):
        if not self.text:
            return
        new_item = dict(text=self.text, id=dt.datetime.now())
        self.set_state(items=self.items + [new_item])

from edifice import Button, Label, TextInput, ScrollView, View

class TodoList(edifice.Component):
    @edifice.register_props
    def __init__(self, items):
        pass

    def render(self):
        return ScrollView()(
            *[Label(f"* {item['text']}").set_key(item['id'])
              for item in self.props.items]
        )

edifice.App(TodoApp()).start()


class GUIEdificeTrain:
    def __init__(self):
        pass