import pandas as pd
import numpy as np
from pathlib import Path
import enum
import pathlib

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.base import BaseEstimator, TransformerMixin
from matplotlib.pyplot import plot, show
import timeit
from sklearn.linear_model import  LinearRegression, Lasso
from sklearn.utils._testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning
from sklearn.preprocessing import KBinsDiscretizer
from mlinsights.mlmodel import PiecewiseRegressor
from Program.Production.config_db import CompanyDictionary


from Program.ObjectBuilders.Parser import *


class GfemDataFrame:
    def __init__(self,
                 file_path: str,
                 ):
        self.file_path = file_path
        self.path = file_path + '\СВОД_Скв_формат из ГФЭМ.xlsm'
        self.parser = GfemParser(data_path=self.path)
        self.company_names = None

    def result(self):
        return self._recalculate_indicators()

    def _data(self) -> pd.DataFrame:
        return self.parser.data()

    def _recalculate_indicators(self):
        data = self._data()
        companydict = CompanyDict(path=self.file_path)
        company_dict = companydict.load(scenario_program=True)
        self.company_names = list(companydict.joint_venture_crude_part.keys())
        prepared_data = pd.DataFrame()
        prepared_data['Месторождение'] = data['Месторождение']
        prepared_data['Скважина'] = data['Скважина']
        prepared_data['Куст'] = data['Куст']
        prepared_data['FCF первый месяц'] = data['FCF первый месяц:']/1000
        prepared_data['НДН за первый месяц; тыс. т'] = data['НДН за первый месяц; тыс. т']
        prepared_data['НДН за первый месяц; т./сут.'] = prepared_data['НДН за первый месяц; тыс. т']/(365/12)*1000
        prepared_data['Уд.FCF на 1 тн. (за 1 мес.)'] = prepared_data['FCF первый месяц']/\
                                                       prepared_data['НДН за первый месяц; т./сут.']
        prepared_data['Доля СП по добыче'] = 1
        prepared_data['Доля СП по FCF'] = 1
        prepared_data['ДО'] = 'ГПН'
        for index, row in prepared_data.iterrows():
            row['ДО'] = company_dict[row['Месторождение']]
            prepared_data.at[index,'ДО'] = company_dict[row['Месторождение']]
            prepared_data.at[index,'Доля СП по добыче'] = companydict.joint_venture_crude_part[row['ДО']]
            prepared_data.at[index,'Доля СП по FCF'] = companydict.joint_venture_fcf_part[row['ДО']]

        prepared_data['НДН за первый месяц; тыс. т. с долей СП'] = prepared_data['НДН за первый месяц; тыс. т'] * prepared_data['Доля СП по добыче']
        prepared_data['FCF первый месяц c долей СП'] = prepared_data['FCF первый месяц'] * prepared_data['Доля СП по FCF']
        prepared_data['НДН за первый месяц; т./сут. с долей СП'] = prepared_data['НДН за первый месяц; тыс. т. с долей СП'] / (365 / 12) * 1000
        prepared_data['Уд.FCF с СП на 1 тн. (за 1 мес.)'] = prepared_data['FCF первый месяц c долей СП']/prepared_data['НДН за первый месяц; т./сут. с долей СП']
        return prepared_data


class PortuDataFrame(GfemDataFrame):
    def __init__(self,
                 file_path: str):
        super().__init__(file_path=file_path)
        self.path = file_path + '\Portu_results.xlsx'
        self.parser = PortuResultsParser(data_path=self.path)
        self.company_names = None

    def _recalculate_indicators(self):

        companydict = CompanyDict(path=self.file_path)
        company_dict = companydict.load(scenario_program=True)
        self.company_names = list(companydict.joint_venture_crude_part.keys())

        data_full = self._data()
        result = []
        for key in data_full:
            data = data_full[key]
            prepared_data = pd.DataFrame()
            prepared_data['Месторождение'] = data['Field']
            prepared_data['ДО'] = data['Suborganization']
            prepared_data['Скважина'] = data['WellNumber']
            prepared_data['Куст'] = data['WellsGroup']
            prepared_data['FCF первый месяц'] = data['FCF; тыс.р.']
            prepared_data['FCF исходный'] = data['FCF исходный; тыс.р.']
            prepared_data['НДН за первый месяц; тыс. т'] = data['Добыча нефти; тыс.т.']
            prepared_data['НДН за первый месяц; т./сут.'] = prepared_data['НДН за первый месяц; тыс. т']/(365/12)*1000
            prepared_data['Уд.FCF на 1 тн. (за 1 мес.)'] = prepared_data['FCF первый месяц']/\
                                                           prepared_data['НДН за первый месяц; т./сут.']
            prepared_data['Добыча нефти, исходная'] = data['Добыча нефти исходный; тыс.т.']
            for index, row in prepared_data.iterrows():
                row['ДО'] = company_dict[row['Месторождение']]
                prepared_data.at[index, 'Доля СП по добыче'] = companydict.joint_venture_crude_part[row['ДО']]
                prepared_data.at[index, 'Доля СП по FCF'] = companydict.joint_venture_fcf_part[row['ДО']]

            prepared_data['НДН за первый месяц; тыс. т. с долей СП'] = prepared_data['НДН за первый месяц; тыс. т'] * prepared_data['Доля СП по добыче']
            prepared_data['FCF первый месяц c долей СП'] = prepared_data['FCF первый месяц'] * prepared_data['Доля СП по FCF']
            prepared_data['НДН за первый месяц; т./сут. с долей СП'] = prepared_data['НДН за первый месяц; тыс. т. с долей СП'] / (365 / 12) * 1000
            prepared_data['Уд.FCF с СП на 1 тн. (за 1 мес.)'] = prepared_data['FCF первый месяц c долей СП']/prepared_data['НДН за первый месяц; т./сут. с долей СП']
            result.append(prepared_data)
        return result


class AroMonitoring:

    def __init__(self,
                 file_path: str,
                 filter: dict = {'Company': 'All', 'Field': 'All'},
                 ):

        self.file_path = file_path
        self.path = file_path + '\gfem_results.db'
        self.parser = GfemDataBaseParser(data_path=self.path,
                                         file_path=self.file_path,
                                         add_data_from_excel=True)
        self.filter = filter
        self.black_list_names = ['id', 'Тип объекта', 'Скважина', 'Куст', 'Объект подготовки','Месторождение', 'ДО', 'Дата внесения', 'Статус по рентабельности']
        self.__monitoring_base = MonitoringSQLSpeakingObject(path=self.path)

    def _data(self) -> pd.DataFrame:
        return self.parser.data()

    def _recalculate_indicators(self):
        data = self._data()

        prepared_data = data
        prepared_data.loc[prepared_data['Тип объекта'].str[0] == 'W', 'Тип объекта'] = 'Скважина'
        prepared_data.loc[prepared_data['Тип объекта'] == 'GROUP_ECONOMIC', 'Тип объекта'] = 'Куст'
        prepared_data.loc[prepared_data['Тип объекта'] == 'PREPARATION_OBJECT_ECONOMIC', 'Тип объекта'] = 'Объект подготовки'
        prepared_data = prepared_data.loc[~prepared_data['Тип объекта'].isin(['GROUP_OPEX','PREPARATION_OBJECT_OPEX'])]

        if self.filter['Company'] != 'All':
            prepared_data = prepared_data.loc[prepared_data['ДО'] == self.filter['Company']]
        if self.filter['Field'] != 'All':
            prepared_data = prepared_data.loc[prepared_data['Месторождение'] == self.filter['Field']]
        prepared_data = prepared_data.drop(columns=['GAP'])

        return prepared_data

    def __prepare_df(self, df: pd.DataFrame, new_data: bool = False):
        df['Скважина'].replace(to_replace=[None], value='-', inplace=True)
        df['Куст'].replace(to_replace=[None], value='-', inplace=True)
        df['Объект подготовки'].replace(to_replace=[None], value='-', inplace=True)
        df['temp_id'] = df.loc[:, 'Скважина'] + df.loc[:,'Скважина'] + df.loc[:, 'Объект подготовки'] + df.loc[:,'Месторождение']
        if new_data:
            df['Дата внесения'] = pd.to_datetime("today")
    #        df['Статус по рентабельности'] = 'Нерентабельная'
        return df

    def black_list(self, excel_export: bool = False):
        db_path = self.file_path + '/monitoring.db'
        db_black_list_data = MonitoringBaseParser(data_path=db_path).data()
   #     db_full_list_data = MonitoringFullParser(data_path=db_path).data()
      #  db_black_list_data = self.__monitoring_base.black_list_from_db()
     #   db_full_list_data = self.__monitoring_base.full_data_black_list_from_db()
        db_black_list_data = self.__prepare_df(df=db_black_list_data)

        data = self._recalculate_indicators()
        data = self.__prepare_df(df=data, new_data=True)

        black_list = data.loc[:, :]

        black_list['temp_id'] = data['Скважина'] + data['Скважина'] + data['Объект подготовки'] + data['Месторождение']

        black_list = black_list.loc[~black_list['temp_id'].isin(db_black_list_data['temp_id'])]
   #     black_list = self.__merge_prep_objects(data=black_list)

   #     black_list = pd.concat([black_list, db_black_list_data])

        export_list = black_list.drop(columns=self.black_list_names[1:-2])
        black_list = black_list.loc[:, self.black_list_names]

        self.__export_black_list(data=black_list, excel_export=excel_export)
        self.__export_full_list(data=export_list, excel_export=excel_export)

    def aro_full_info_black_list(self, path: str=None, excel_export: bool = False):
        if path is None:
            path = self.file_path
        data = self._recalculate_indicators()

        export_list = data.drop(columns=self.black_list_names[1:-2])
        export_list = export_list.drop(columns='Лицензионный участок')
        self.__export_full_list(data=export_list, excel_export=excel_export)

    def __export_black_list(self, data: pd.DataFrame, excel_export: bool):
        if excel_export:
            BlackListLoaderExcel(data=data, source_path=self.file_path).load_data()

        BlackListLoaderDB(data=data, source_path=self.file_path).load_data()

    def __export_full_list(self, data: pd.DataFrame, excel_export: bool):
        if excel_export:
            data.to_excel(self.file_path + '/Full_list.xlsx')
        data =data.drop(
            columns=['Лицензионный участок', 'temp_id', 'Дата внесения', 'Статус по рентабельности',])
        #data = data.drop(columns=['Статус по рентабельности', 'Дата внесения'])
        AROFullLoaderDB(data=data, source_path=self.file_path).load_data()
        self.parser.transfer_month_table(path=self.file_path)

    def export_company_form(self):
        db_path = self.file_path + '/monitoring.db'
        parser = MonitoringBaseParser(data_path=db_path)
        prepared_data = parser.data()
        if self.filter['Company'] != 'All':
            prepared_data = prepared_data.loc[prepared_data['ДО'] == self.filter['Company']]
        if self.filter['Field'] != 'All':
            prepared_data = prepared_data.loc[prepared_data['Месторождение'] == self.filter['Field']]
        prepared_data['Мероприятие'] = ''
        prepared_data['Комментарии к мероприятию'] = ''
        prepared_data['Дата выполнения мероприятия (План)'] = ''
        prepared_data['Дата выполнения мероприятия (Факт)'] = ''
        prepared_data['Отвественный(название должности)'] = ''
        prepared_data['Статус. В работе/остановлена'] = ''
        prepared_data['Наличие отказа. Да/Нет'] = ''
        prepared_data.drop(columns=['Дата внесени2я', 'id'])
        prepared_data.to_excel(self.file_path + '\Форма для ДО.xlsx')

    def load_company_form_to_db(self, data: pd.DataFrame):
        db_path = self.file_path + '/monitoring.db'
        db_activity_data = MonitoringActivityParser(data_path=db_path).data()
       # db_activity_data
       # data = data.loc[~data['id'].isin(db_activity_data['object_id'].isin(data['id']))]

        export_data = data[['id', 'Мероприятие', 'Комментарии к мероприятию',
                                'Дата выполнения мероприятия (План)', 'Дата выполнения мероприятия (Факт)',
                                'Отвественный (название должности)', 'Статус. В работе/остановлена',
                                'Наличие отказа. Да/Нет', ]]
        ActivityLoaderDB(data=export_data, source_path=self.file_path).load_data()

class SortedGfemData:

    def __init__(self,
                 prepared_data: GfemDataFrame,
                 ):
        self.prepared_data = prepared_data
        self.company_names = None

    def _data(self):
        return self.prepared_data.result()

    def result(self):
        dataframe = self._data()
        company_names = self.prepared_data.company_names
        self.company_names = company_names
        result_data = []
        result_jv = []
        result_data.append(dataframe.sort_values(by='Уд.FCF на 1 тн. (за 1 мес.)'))
        result_jv.append(dataframe.sort_values(by='Уд.FCF с СП на 1 тн. (за 1 мес.)'))
        for name in company_names:
            result = dataframe.loc[dataframe['ДО'] == name]
            result_data.append(result.sort_values(by='Уд.FCF на 1 тн. (за 1 мес.)'))
            result_jv.append(result.sort_values(by='Уд.FCF с СП на 1 тн. (за 1 мес.)'))

        return {'Без учета СП': result_data, 'C учетом СП': result_jv}


class RegressionScenarios:

    def __init__(self,
                 sorted_data: SortedGfemData):
        self.sorted_data = sorted_data
        self.company_names = None
        self.dataframe = []
    def _data(self):
        data = self.sorted_data.result()
        self.company_names = self.sorted_data.company_names.copy()

        return data

    def scenarios(self):
        data = self.data_for_regression()
        full_scenarios = {}
        jv_scenarios = {}
        full_scenarios['ГПН'] = self._prepare_scenario(data=data[0][0].to_numpy())
        jv_scenarios['ГПН'] = self._prepare_scenario(data=data[1][0].to_numpy())
        for i in range(len(self.company_names)):
            full_scenarios[self.company_names[i]] = self._prepare_scenario(data=data[0][i+1].to_numpy())
            jv_scenarios[self.company_names[i]] = self._prepare_scenario(data=data[1][i + 1].to_numpy())

        return [full_scenarios, jv_scenarios]

    @ignore_warnings(category=ConvergenceWarning)
    def _prepare_scenario(self, data):
        data1 = np.copy(data)
        x_initial = data1.T[0]
        y_initial = data1.T[1]
        x1 = np.cumsum(x_initial)
        x = x1[:, np.newaxis]
        y = np.cumsum(y_initial)

        X_train, X_test, Y_train, Y_test = train_test_split(x, y,
                                                            test_size=1,
                                                            random_state=1)

        poly_model = PiecewiseRegressor(verbose=True,
                                        binner=KBinsDiscretizer(n_bins=40))
     #   poly_model = LinearRegression()

        poly_model.fit(X_train, Y_train)

        return [poly_model, x.min(), x.max()]

    def data_for_regression(self):
        data = self._data()
        full_data = data['Без учета СП']
        self.dataframe.append(full_data[0])
        jv_data = data['C учетом СП']
        self.dataframe.append(jv_data[0])
        result_full = []
        result_jv = []
        for dataframe in full_data:
            result_full.append(dataframe[['НДН за первый месяц; т./сут.', 'FCF первый месяц']])

        for dataframe in jv_data:
            result_jv.append(dataframe[['НДН за первый месяц; т./сут. с долей СП', 'FCF первый месяц c долей СП']])

        return [result_full, result_jv]


class SolutionBalancer:

    def __init__(self,
                 dataframe_list: list,
                 company_names: list,
                 ):
        self.dataframe_list = dataframe_list
        self.company_names = company_names
        self.data_for_excel = pd.DataFrame()

    def result(self, crude_value: float, solution_index: int, company_name: list = ['All'], company_value: list = [0.0]):
        dataframe = self.dataframe_list[solution_index]

        if solution_index == 0:
            key = 'НДН за первый месяц; т./сут.'
        if solution_index == 1:
            key = 'НДН за первый месяц; т./сут. с долей СП'
        if company_name[0] != 'All':
            temp_dataframe = dataframe
            company_filtered_dataframe = pd.DataFrame()
            for i in range(len(company_name)):

                company_dataframe = temp_dataframe.loc[temp_dataframe['ДО'] == company_name[i]]
                company_result = company_dataframe[[key]].to_numpy()
                company_data = np.copy(company_result)
                x_initial = company_data.T[0]
                x = np.cumsum(x_initial)
                array_index = np.searchsorted(x, company_value[i], side="right")
                company_filtered_dataframe = pd.concat([company_filtered_dataframe, company_dataframe.iloc[:array_index+1]])
                dataframe = dataframe.loc[dataframe['ДО'] != company_name[i]]

        result_data = dataframe[[key]].to_numpy()
        data1 = np.copy(result_data)
        x_initial = data1.T[0]
        x = np.cumsum(x_initial)
        array_index = np.searchsorted(x, crude_value-sum(company_value), side="right")
        try:
            filtered_dataframe = dataframe.iloc[:array_index+1]
        except:
            filtered_dataframe = dataframe.iloc[:array_index]
        if company_name[0] == 'All':
            self.data_for_excel = filtered_dataframe
        else:
            self.data_for_excel = pd.concat([filtered_dataframe, company_filtered_dataframe])
        temp_data = []
        for name in self.company_names:
            if name in company_name:
               i = company_name.index(name)
               new_value = company_value[i]
            else:
                x_filtered = filtered_dataframe.loc[filtered_dataframe['ДО'] == name][[key]].to_numpy()
                x_cum = np.cumsum(x_filtered)
                try:
                    new_value = x_cum[-1]
                except IndexError:
                    new_value = 0
            temp_data.append(float(new_value))

        return temp_data

    def _data(self):
        pass

    def export_results(self, path=None):
        if path is None:
            print('Не задан путь к файлу!')
        else:
            self.data_for_excel.to_excel(path)


class CompanyDict:
    def __init__(self,
                 path
                 ):
        self.path = Path(path)
        self.joint_venture_crude_part = {}
        self.joint_venture_fcf_part = {}

    def load(self, scenario_program: bool = False):
        if not scenario_program:
            DATA = self.path / 'Балансировка компенсационных мероприятий для НРФ.xlsm'
        else:
            DATA = self.path / 'Словарь ДО.xlsx'
        df = pd.read_excel(DATA, sheet_name='Словарь ДО')

        df1 = df['Список ДО']
        df2 = df['Месторождение']
        if scenario_program:
            dataframe = pd.read_excel(DATA, sheet_name='Доли СП')
            df3 = dataframe['ДО']
            df4 = dataframe['По добыче']
            df5 = dataframe['По FCF']

            self.joint_venture_crude_part = dict(zip(list(df3), list(df4)))
            self.joint_venture_fcf_part = dict(zip(list(df3), list(df5)))
        company_dict = dict(zip(list(df2), list(df1)))
        return company_dict


class Constraints:
    def __init__(self,
                 path,
                 ):
        self.path = Path(path)
        self.dataframe = None
        self.months = None

    def _data(self):
        self.dataframe = pd.read_excel(self.path/'Ограничения.xlsx', )

    def load_constraints(self):
        self._data()
        self.months_index=self.dataframe.columns[1:]
        self.months = np.datetime_as_string(np.array(self.dataframe.columns[1:], dtype='datetime64'), unit='M')

    def extract_value(self, index: int):
        return self.dataframe[self.months_index[index]].iloc[22]*1000

    def extract_list(self, index: int):
        return self.dataframe[self.months_index[index]]*1000

