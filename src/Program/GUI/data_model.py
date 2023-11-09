from Program.GUI.data_value import DataValue

import numpy as np
import pandas as pd
from copy import deepcopy, copy
from typing import Callable

from Program.AROMonitoring.aro_monitoring import AroMonitoring
from Program.Production.GfemScenarios import *
from Program.Production.config_db import CompanyDictionary

from edifice import Label,  Slider, Dropdown, View, CheckBox,TextInput,  Component, StateManager, Window, Button, ScrollView
from edifice.components.forms import FormDialog, Form
from edifice.components import plotting
from edifice import Timer


class DataModelPortu:
    def __init__(self, path):
        self.path = path
        self.__db_name = self.path + '/balancer_results.db'


class DataModel:
    def __init__(self,
                 scenarios: RegressionScenarios,
                 path: str = None,
            ):

        self.scenarios = scenarios
        self.path = Path(path)

        self.company_value = DataValue('0')
        self.company_fcf = DataValue('0')

        self.vostok_value = DataValue('0.0')
        self.megion_value = DataValue('0.0')
        self.messoyaha_value = DataValue('0.0')
        self.nng_value = DataValue('0.0')
        self.orenburg_value = DataValue('0.0')
        self.hantos_value = DataValue('0.0')
        self.yamal_value = DataValue('0.0')
        self.crude_sum = DataValue('0')

        self.shelf_value = DataValue('0')
        self.polar_value = DataValue('0')
        self.meretoyaha_value = DataValue('0')
        self.palyan_value = DataValue('0')
        self.spd_value = DataValue('0')
        self.arctic_value = DataValue('0')
        self.angara_value = DataValue('0')

        self.shelf_fcf = DataValue('-')
        self.polar_fcf = DataValue('-')
        self.meretoyaha_fcf = DataValue('-')
        self.palyan_fcf = DataValue('-')
        self.spd_fcf = DataValue('-')
        self.arctic_fcf = DataValue('-')
        self.angara_fcf = DataValue('-')

        self.forecast_sum = DataValue('0')
        self.result_crude_sum = DataValue('0')
        self.quota = DataValue('0.0')

        self.vostok_fcf = DataValue('0.0')
        self.megion_fcf = DataValue('0.0')
        self.messoyaha_fcf = DataValue('0.0')
        self.nng_fcf = DataValue('0.0')
        self.orenburg_fcf = DataValue('0.0')
        self.hantos_fcf = DataValue('0.0')
        self.yamal_fcf = DataValue('0.0')
        self.fcf_sum = DataValue('0.0')

        self.full_company_list = []
        self.forecast_list = []
        self.crude_list = []
        self.result_crude_list = []

        self.joint_venture = False

        self.__constraints = None
        self.__data = None
        self.company_names = None
        self.__solution = None
        self.__dataframe_list = None
        self.months = None
        self.__control_option = False
        self.control_option = False

        self.__min_value_full = {}
        self.__max_value_full = {}

        self.__min_value_jv = {}
        self.__max_value_jv = {}

        self.min_value = {}
        self.max_value = {}

        self.index = 0
        self.target = DataValue('0')

        self.__last_company_value = [0]
        self.__last_company = ['All']
        self.__last_target = 0.0

    def pie_plot_coordinates(self):
        values = self.__do_values_for_plot()
        x = []
        for value in values:
            x.append((value+0.0001)/(self.company_value.toFloat+0.0001))
        new_values = [i for i in values]
        return x, new_values

    def plot_coordinates(self):
        if self.joint_venture:
            j = 1
            key = 'НДН за первый месяц; т./сут. с долей СП'
            key2 ='Уд.FCF с СП на 1 тн. (за 1 мес.)'
        else:
            j = 0
            key = 'НДН за первый месяц; т./сут.'
            key2 = 'Уд.FCF на 1 тн. (за 1 мес.)'
        temp_dataframe = self.__dataframe_list[j]

        x = {}
        y = {}
        x2 = {}
        y2 = {}

        values = self.__do_values_for_plot()
        value = 0
        for name in self.company_names:

            x2[name] = (np.linspace(1, values[value]+1.1, 300))
            y2[name] = self.__data[j][name][0].predict(x2[name][:, np.newaxis])
            x2[name] = x2[name]#*30.43/1000
        #    y2[name] = y2[name]/x2[name]

            company_dataframe = temp_dataframe.loc[temp_dataframe['ДО'] == name]
            company_result = company_dataframe[[key]].to_numpy()
            company_data = np.copy(company_result)
            x_initial = company_data.T[0]
            x_j = np.cumsum(x_initial)
            array_index = np.searchsorted(x_j, values[value], side="right")
            if array_index == 0:
                result = 0
            else:
                try:
                    result = company_dataframe[key2].iloc[array_index]
                except IndexError:
                    result = company_dataframe[key2].iloc[-1]

            value += 1
            y2[name] = result
            x[name] = x_j
            y[name] = company_dataframe[key2]

        for name in self.company_names:
        #    x[name] = (np.linspace(1, self.max_value[name].toFloat ,300))
          #  y[name] = self.__data[j][name][0].predict(x[name][:, np.newaxis])
            x[name] = x[name]#*30.43/1000
         #   y[name] = y[name]/x[name]
        #    y2[name] = np.cumsum(y[name])/(np.cumsum(x[name])+0.001)

        #    y[name] = y[name]/(x[name]+0.01)
        """
        self.vostok_value = DataValue('0.0')
        self.megion_value = DataValue('0.0')
        self.messoyaha_value = DataValue('0.0')
        self.nng_value = DataValue('0.0')
        self.orenburg_value = DataValue('0.0')
        self.hantos_value = DataValue('0.0')
        self.yamal_value = DataValue('0.0')
        
        if self.__last_company[-1] =='All':
            x = np.linspace(0, self.max_value[name].toFloat, 100)
            y = self.__data[j][name][0].predict(x[:, np.newaxis])

            x2 = np.linspace(0, self.company_value.toFloat, 100)
            y2 = self.__data[j][name][0].predict(x2[:, np.newaxis])

        else:
            x = np.linspace(0, self.max_value[self.__last_company[-1]].toFloat, 100)
            y = self.__data[j][self.__last_company[-1]][0].predict(x[:, np.newaxis])

            x2 = np.linspace(0, self.__last_company_value[-1], 100)
            y2 = self.__data[j][self.__last_company[-1]][0].predict(x2[:, np.newaxis])
        """
        return x, y, x2, y2

    def initializtion(self):
        self.__data = self.scenarios.scenarios()
        self.__constraints = Constraints(path=self.path)
        self.__constraints.load_constraints()

        self.company_names = self.scenarios.company_names.copy()

        self.company_names_full = self.company_names.copy()
        self.company_names_full.append('Шельф')
        self.company_names_full.append('Заполярье')
        self.company_names_full.append('Меретояханефтегаз')
        self.company_names_full.append('Пальян')
        self.company_names_full.append('СПД')
        self.company_names_full.append('Арктикгаз')
        self.company_names_full.append('Ангара')


        self.__min_value_full['ГПН'] = DataValue(str(0))
        self.__max_value_full['ГПН'] = DataValue(str(self.__data[0]['ГПН'][2]))
        self.__min_value_jv['ГПН'] = DataValue(str(0))
        self.__max_value_jv['ГПН'] = DataValue(str(self.__data[1]['ГПН'][2]))

        for name in self.company_names:
            self.__min_value_full[name] = DataValue(str(0))
            self.__max_value_full[name] = DataValue(str(self.__data[0][name][2]))

            self.__min_value_jv[name] = DataValue(str(0))
            self.__max_value_jv[name] = DataValue(str(self.__data[1][name][2]))
        names = ['Заполярье', 'Шельф', 'Меретояханефтегаз', 'Пальян', 'СПД', 'Арктикгаз', 'Ангара']
        for name in names:
            self.__max_value_full[name] = DataValue(str(1))
            self.__max_value_jv[name] = DataValue(str(1))
        self.__dataframe_list = self.scenarios.dataframe
        self.__solution = SolutionBalancer(dataframe_list=self.__dataframe_list,
                                           company_names=self.company_names_full)
        self.target = DataValue(str(self.__constraints.extract_value(index=self.index)))
        self.months = self.__constraints.months

        self.full_company_list = self.__company_result_list()

        self.forecast_list = self.__constraints.extract_list(index=self.index)
        self.__load_min_max_for_other_companies(forecast_list=self.forecast_list)

        self.crude_list = self.__do_result_list()
        self.result_crude_list = self.__result_crude_list()

        self.choose_scenario()

    def __load_min_max_for_other_companies(self, forecast_list):
        names = ['Заполярье', 'Шельф', 'Меретояханефтегаз',  'Пальян', 'СПД', 'Арктикгаз', 'Ангара']
        for name in names:
            self.__min_value_full[name] = DataValue(str(0))
            self.__min_value_jv[name] = DataValue(str(0))

        forecast_names = [3,0,4,7,12,14,19]
        for i in range(len(forecast_names)):
            if forecast_list[forecast_names[i]] == 0:
                value = round(forecast_list[forecast_names[i]],1) + 1
            else:
                value = round(forecast_list[forecast_names[i]],1)
            self.__max_value_full[names[i]].update(value)
            self.__max_value_jv[names[i]].update(value)

    def choose_scenario(self, value: bool = None):

        self.joint_venture = not self.joint_venture

        if self.joint_venture:
            self.min_value = self.__min_value_jv
            self.max_value = self.__max_value_jv

        else:
            self.min_value = self.__min_value_full
            self.max_value = self.__max_value_full

        self.plot_coordinates()

    def __company_result_list(self):
        company_result_list = self.__constraints.dataframe['ДО'].iloc[:23].to_list()
        return company_result_list

    def __do_values_for_plot(self):
        return [self.vostok_value.toFloat,
                self.megion_value.toFloat,
                self.messoyaha_value.toFloat,
                self.nng_value.toFloat,
                self.orenburg_value.toFloat,
                self.hantos_value.toFloat,
                self.yamal_value.toFloat]

    def __do_result_list(self):
        result = [self.vostok_value.toFloat,
                self.megion_value.toFloat,
                self.messoyaha_value.toFloat,
                self.nng_value.toFloat,
                self.orenburg_value.toFloat,
                self.hantos_value.toFloat,
                self.yamal_value.toFloat]

        return [self.shelf_value.toFloat,
                result[0],0,self.polar_value.toFloat, self.meretoyaha_value.toFloat,
                result[2],
                result[4],self.palyan_value.toFloat,
                result[1],
                result[5],
                result[6],
                result[3],
                self.spd_value.toFloat, 0, self.arctic_value.toFloat,0,0,0,0,self.angara_value.toFloat,]

    def __result_crude_list(self):
        result_crude = np.array(self.forecast_list)[
                        0:len(self.__do_result_list())] - np.array(self.__do_result_list())
        return result_crude

    def choose_month(self, value):
    #    self.control_option = False
        self.index = int(np.where(self.__constraints.months == value)[0])
        val = self.__constraints.extract_value(index=int(np.where(self.__constraints.months == value)[0]))
        self.forecast_list = self.__constraints.extract_list(index=self.index)

        self.__load_min_max_for_other_companies(forecast_list=self.forecast_list)
        self.target.update(val)
        self.forecast_sum.update(self.__constraints.extract_list(index=self.index)[20])
        self.set_value(company_value=val)
        new_values = self._find_solution(target=val)
        self.__update_values_for_view(new_values)
        self.quota.update(self.__constraints.extract_list(index=self.index).iloc[21])

    def on_click(self):
        self.__control_option = False

    def __control(self, company, value):
        self.__control_option = False
        if self.__last_company[0] == 'All':
            self.__last_company_value = []
            self.__last_company = []
        self.control_option = False
        if company not in self.__last_company:
            self.__last_company.append(company)
            self.__last_company_value.append(value)
        else:
            i = self.__last_company.index(company)
            self.__last_company[i] = company
            self.__last_company_value[i] = value

    def set_value(self, company_value):
        self.__control_option = True
        self.__last_company = []
        self.__last_company.append('All')
        self.__last_company_value = []
        self.__last_company_value.append(0)
        self.__last_target = company_value
        self.company_value.update(company_value)
        self.shelf_value.update(0)
        self.polar_value.update(0)
        self.meretoyaha_value.update(0)
        self.palyan_value.update(0)
        self.spd_value.update(0)
        self.arctic_value.update(0)
        self.angara_value.update(0)

    def reset_results(self):
        self.on_gpn_change(company_value=self.__last_target)

    def on_gpn_change(self, company_value):
        self.set_value(company_value)
        new_values = self._find_solution(target=company_value)

        self.__update_values_for_view(new_values)

    def set_vostok_value(self, value):
        value = self.__check_value(value=value, company=self.company_names[0])
        self.vostok_value.update(value)
        self.__control(company=self.company_names[0],value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def set_megion_value(self, value):
        value = self.__check_value(value=value, company=self.company_names[1])
        self.megion_value.update(value)
        self.__control(company=self.company_names[1], value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def set_messoyaha_value(self, value):
        value = self.__check_value(value=value, company=self.company_names[2])
        self.messoyaha_value.update(value)
        self.__control(company=self.company_names[2], value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def set_nng_value(self, value):

        value = self.__check_value(value=value, company = self.company_names[3])
        self.nng_value.update(value)
        self.__control(company=self.company_names[3], value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def set_orenburg_value(self, value):
        value = self.__check_value(value=value, company=self.company_names[4])
        self.orenburg_value.update(value)
        self.__control(company=self.company_names[4], value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def set_hantos_value(self, value):
        value = self.__check_value(value=value, company=self.company_names[5])
        self.hantos_value.update(value)
        self.__control(company=self.company_names[5], value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def set_yamal_value(self, value):
        value = self.__check_value(value=value, company=self.company_names[6])
        self.yamal_value.update(value)
        self.__control(company=self.company_names[6], value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def set_polar_value(self, value):
        value = self.__check_value(value=value, company='Заполярье')
        self.polar_value.update(value)
        self.__control(company='Заполярье', value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def set_meretoyaha_value(self, value):
        value = self.__check_value(value=value, company='Меретояханефтегаз')
        self.meretoyaha_value.update(value)
        self.__control(company='Меретояханефтегаз', value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def set_spd_value(self, value):
        value = self.__check_value(value=value, company='СПД')
        self.spd_value.update(value)
        self.__control(company='СПД', value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def set_shelf_value(self, value):
        value = self.__check_value(value=value, company='Шельф')
        self.shelf_value.update(value)
        self.__control(company='Шельф', value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def set_arctic_value(self, value):
        value = self.__check_value(value=value, company='Арктикгаз')
        self.arctic_value.update(value)
        self.__control(company='Арктикгаз', value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def set_palyan_value(self, value):
        value = self.__check_value(value=value, company='Пальян')
        self.palyan_value.update(value)
        self.__control(company='Пальян', value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def set_angara_value(self, value):
        value = self.__check_value(value=value, company='Ангара')
        self.angara_value.update(value)
        self.__control(company='Ангара', value=value)
        new_values = self._find_solution(target=self.__last_target,
                                         company_name=self.__last_company,
                                         company_value=self.__last_company_value)
        self.__update_values_for_view(new_values)

    def __update_values_for_view(self, values):
        self.company_value.update(self.__last_target)
        self.crude_sum.update(sum(values))

        self.vostok_value.update(values[0])
        self.megion_value.update(values[1])
        self.messoyaha_value.update(values[2])
        self.nng_value.update(values[3])
        self.orenburg_value.update(values[4])
        self.hantos_value.update(values[5])
        self.yamal_value.update(values[6])
        self.shelf_value.update(values[7])
        self.polar_value.update(values[8])
        self.meretoyaha_value.update(values[9])
        self.palyan_value.update(values[10])
        self.spd_value.update(values[11])
        self.arctic_value.update(values[12])
        self.angara_value.update(values[13])

        self.crude_list = self.__do_result_list()

        fcf = self._update_fcf(values=values)
        self.fcf_sum.update(fcf.sum())
        self.company_fcf.update(fcf.sum())
        self.company_fcf.update(fcf.sum())
        self.vostok_fcf.update(fcf[0])
        self.megion_fcf.update(fcf[1])
        self.messoyaha_fcf.update(fcf[2])
        self.nng_fcf.update(fcf[3])
        self.orenburg_fcf.update(fcf[4])
        self.hantos_fcf.update(fcf[5])
        self.yamal_fcf.update(fcf[6])
        self.shelf_fcf.update(fcf[7])
        self.polar_fcf.update(fcf[8])
        self.meretoyaha_fcf.update(fcf[9])
        self.palyan_fcf.update(fcf[10])
        self.spd_fcf.update(fcf[11])
        self.arctic_fcf.update(fcf[12])
        self.angara_fcf.update(fcf[13])

        self.result_crude_list = self.__result_crude_list()
        self.result_crude_sum.update(sum(self.result_crude_list))

    def _update_company_fcf(self, value, i):
        if self.joint_venture:
            j = 1
        else:
            j = 0

        if value == 0:
            fcf = 0
        else:
            fcf = self.__data[j][self.company_names[i]][0].predict(np.array(value).reshape(-1, 1))
        return float(fcf)

    def _update_fcf(self, values):
        fcf = np.zeros_like(values)
        if self.joint_venture:
            j = 1
        else:
            j = 0

        for i in range(len(values)):
            if values[i] == 0:
                fcf[i] = 0
            else:
                try:
                    fcf[i] = self.__data[j][self.company_names[i]][0].predict(np.array(values[i]).reshape(-1, 1))
                except:
                    fcf[i] = 0
        if self.company_value.toFloat == 0:
            self.company_fcf = DataValue('0')
        return fcf

    def _find_solution(self, company_name: list = ['All'], company_value: list = [0.0], target: float = 0):
        print(self.joint_venture)
        if self.joint_venture:
            j = 1
        else:
            j = 0
        if self.__control_option:
            new_values = self.__solution.result(crude_value=target,
                                                solution_index=j)
        else:
            new_values = self.__solution.result(crude_value=target,
                                                solution_index=j,
                                                company_name=company_name,
                                                company_value=company_value)

        for i in range(len(new_values)):
            if self.max_value[self.company_names_full[i]].toFloat < new_values[i]:
                new_values[i] = self.max_value[self.company_names_full[i]].toFloat
            if self.min_value[self.company_names_full[i]].toFloat > new_values[i]:
                new_values[i] = self.min_value[self.company_names_full[i]].toFloat

        return new_values

    def __check_value(self, value, company):
        if self.__last_company[-1] != 'All':
            try:
                i = self.__last_company.index(company)
            except:
                i = 50
            summa = self.__last_target
            val = 0
            for j in range(len(self.__last_company_value)):
                if j != i:
                    val = val + self.__last_company_value[j]
            if summa < (val + value):
                value = summa - val
        return value

    def save_results(self, path):
        self.__solution.export_results(path=path)

    def save_overal_results(self, path):
        if self.joint_venture:
            j = 1
        else:
            j = 0
        self.__solution.export_overal_results(path=path, solution_index=j, month=self.__constraints.months[self.index])


class DataModelFull(DataModel):
    def __init__(self,
                 scenarios: RegressionScenarios,
                 portu_results: PortuDataFrame,
                 path: str = None,
                 ):
        self.str_path = path
        super().__init__(scenarios=scenarios, path=path)
        self.portu_results = portu_results
        self.portu_names = ['ООО "ГПН-Восток"',  'ПАО_СН_МНГ', 'АО «Мессояханефтегаз»',
                            'AO «ГПН-ННГ»', 'ООО "ГПН-Оренбург"',
                             'ООО "ГПН-Хантос"', 'ООО "ГПН - Ямал"',]
        self.crude_volume = {}
        self.fcf_volume = {}
        self.fcf_values = []

    def full_initializtion(self):
        self.initializtion()
        self.portu_results = self.portu_results.result()

        df = pd.read_excel(self.str_path + '\Данные_по_объектам_для_балансировки_5тилетка.xlsx')
        i = 0
        crude_col = ['Crude 1',	'Crude 2',	'Crude 3',	'Crude 4',	'Crude 5',	'Crude 6',	'Crude 7',	'Crude 8',	'Crude 9',	'Crude 10']
     #   fcf_col = ['FCF 1',	'FCF 2',	'FCF 3',	'FCF 4',	'FCF 5',	'FCF 6',	'FCF 7',	'FCF 8',	'FCF 9',	'FCF 10']
        days = [31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for name in self.company_names:
           temp_df = df.loc[df['ДО'] == self.portu_names[i]]
           crude_list = []
       #    fcf_list = []
           for j in range(10):
               a = temp_df[crude_col[j]].to_numpy().sum()
               crude_list.append(a/days[j]*1000)
       #        fcf_list.append(temp_df[fcf_col[j]].to_numpy().sum())
           self.crude_volume[name] = crude_list
        #   self.fcf_volume[name] = fcf_list
           i += 1



    def __get_values_from_portu(self, month: int, solution_index: int = 0):
        new_values = []
        fcf_values = []
        days = [31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if solution_index == 0:
            key = 'НДН за первый месяц; т./сут.'

            key = 'НДН за первый месяц; тыс. т'
        if solution_index == 1:
            key = 'НДН за первый месяц; т./сут. с долей СП'
        df = self.portu_results[month]
        for name in self.portu_names:
            temp_df = df.loc[df['ДО'] == name]
            new_values.append(temp_df[key].sum()/days[month]*1000) #- temp_df['Добыча нефти, исходная'].sum()/days[month]*1000)
            fcf_values.append(temp_df['FCF исходный'].sum() - temp_df['FCF первый месяц'].sum() )

        i = 0
        for name in self.company_names:
            new_values[i] = self.crude_volume[name][month]-new_values[i]
      #      fcf_values[i] = self.fcf_volume[name][month]-fcf_values[i]
            i += 1
        for i in range(7):
            new_values.append(0)
            fcf_values.append(0)

        return new_values, fcf_values

    def _update_fcf(self, values):
        return np.array(self.fcf_values)/1000

    def _find_solution(self, company_name: list = ['All'], company_value: list = [0.0], target: float = 0):

        if self.index >= 2:
           index = self.index - 2
        else:
           index = 2

        new_values, fcf_values = self.__get_values_from_portu(month=index)
        self.fcf_values = fcf_values

        for i in range(len(new_values)):
            if self.max_value[self.company_names_full[i]].toFloat < new_values[i]:
                new_values[i] = self.max_value[self.company_names_full[i]].toFloat
            if self.min_value[self.company_names_full[i]].toFloat > new_values[i]:
                new_values[i] = self.min_value[self.company_names_full[i]].toFloat
        return new_values


class DataModelMonitoring:
    def __init__(self,
                 monitoring_module: AroMonitoring):
        self.__monitoring_module = monitoring_module
        self.excel_export = False

      #  self.__field_list ={ 'ГПН-ННГ': ['Все месторождения', 'Еты-пуровское'] }
        self.field = 'Все месторождения'
        self.field_list_for_view = ['Все месторождения']
      #  self.company_dict = CompanyDict(path=self.__monitoring_module.file_path).load(scenario_program=True)
        self.company_dict = CompanyDictionary.names
        self.do_list = list(sorted(set(self.company_dict.values())))
        self.do_list.insert(0, 'Все ДО')
        self.__field_list = {}
        self.__company = 'All'


        for name in self.do_list:
            self.__field_list[name] = ['Все месторождения']
            for key in self.company_dict:
                if name == self.company_dict[key]:
                    self.__field_list[name].append(key)

        print(self.do_list,  self.__field_list)

    def excel_export_option(self):
        self.excel_export = not self.excel_export

    def set_field(self, value):
        self.field = value
        self.__monitoring_module.filter['Company'] = self.__company
        self.__monitoring_module.filter['Field'] = value

    def set_do(self, value):
        self.field_list_for_view = self.__field_list[value]
        self.__company = value
        if value == 'Все ДО': value = 'All'
        self.__monitoring_module.filter['Company'] = value
        self.__monitoring_module.filter['Field'] = 'All'

    def company_form(self):
        self.__monitoring_module.export_company_form()

    def black_list(self):
        self.__monitoring_module.black_list(excel_export=self.excel_export)
    #    self.__monitoring_module.aro_full_info_black_list(excel_export=False)

    def aro_full_info_black_list(self):
        self.__monitoring_module.aro_full_info_black_list(excel_export=self.excel_export)

    def import_company_form(self, file_path: pathlib.Path):
        data = pd.read_excel(file_path)
        self.__monitoring_module.load_company_form_to_db(data)

    def upload_data_for_dashboard(self):
        self.__monitoring_module.upload_data_for_dashboard()

    def map_status_from_mor_db(self,):
        self.__monitoring_module.map_status_from_mor_db()

