from Program.GUI.data_value import DataValue
from Program.GUI.data_model import DataModel
from Program.ObjectBuilders.sql_speaking_objects import BalancerResultsSpeakingObject
import numpy as np
import pandas as pd
from copy import deepcopy, copy
from typing import Callable

from Program.AROMonitoring.aro_monitoring import AroMonitoring
from Program.Production.GfemScenarios import *
from Program.Production.config_db import CompanyDictionary
from Program.ObjectBuilders.Parser import SetOfWellsParserMonth

from edifice import Label,  Slider, Dropdown, View, CheckBox,TextInput,  Component, StateManager, Window, Button, ScrollView
from edifice.components.forms import FormDialog, Form
from edifice.components import plotting
from edifice import Timer



class DataModel:
    def __init__(self,
                 scenarios: RegressionScenarios,
                 path: str = None,
                 five_year_format: bool = True,
                 vbd: bool = False,
            ):

        self.__vbd = vbd
        self.scenarios = scenarios
        self.vbd_scenarios = scenarios
        self.path = Path(path)
        self.__path_str = path
        self.__five_year_format = five_year_format


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
        self.__five_year_scenarios = {}

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

        self.__init_data = None
        self.__init_dataframe_list = []
        self.__five_year_parser = None

        self.__model = {'vbd': {}, 'origin':{}}
        self.model_type = False

    def reset_values(self):
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

            x2[name] = np.array(values[value])
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

        return x, y, x2, y2

    def initializtion(self):
        self.__data = self.scenarios.scenarios()
        self.__init_data = self.__data.copy()
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
        self.__max_value_full['ГПН'] = DataValue('176219')
        self.__max_value_jv['ГПН'] = DataValue(str(self.__data[1]['ГПН'][2]))
        self.__max_value_jv['ГПН'] = DataValue('176219')

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
        self.__init_dataframe_list = self.__dataframe_list.copy()

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
        if self.__five_year_format:
         try:
            self.__five_year_parser_orig = SetOfWellsParserMonth(data_path=self.__path_str, vbd=False)
            self.__five_year_parser_orig.read_excel()
            print('Формат пятилетки прочитан')
            self.__five_year_scenarios_orig = {}
            for month in self.months:

                self.__five_year_parser_orig.set_month(month=month)
                self.__five_year_scenarios_orig[month] = {}
                self.__five_year_scenarios_orig[month]['RegressionScenario'] = RegressionScenarios(sorted_data=SortedGfemData(
                    vbd=False,
                    prepared_data=GfemDataFrame(
                        parser=self.__five_year_parser,
                        file_path=self.__path_str)))

                self.__five_year_scenarios_orig[month]['Data'] = self.__five_year_scenarios_orig[month]['RegressionScenario'].scenarios()
                self.__five_year_scenarios_orig[month]['DataframeList'] = self.__five_year_scenarios_orig[month]['RegressionScenario'].dataframe

            self.__model['origin']['scenario'] = self.__five_year_scenarios_orig
            self.__five_year_scenarios = self.__model['origin']['scenario']

         except KeyError as e:
                print(e)
                print('ошибка свода в формате пятилетки')
         except:
                print('ошибка свода в формате пятилетки')

        if self.__vbd:
            try:
                self.__five_year_parser_vbd = SetOfWellsParserMonth(data_path=self.__path_str, vbd=True)
                self.__five_year_parser_vbd.read_excel()
                print('Формат пятилетки ВБД прочитан')
                self.__five_year_scenarios_vbd = {}
                for month in self.months:
                    self.__five_year_parser_vbd.set_month(month=month)
                    self.__five_year_scenarios_vbd[month] = {}
                    self.__five_year_scenarios_vbd[month]['RegressionScenario'] = RegressionScenarios(
                        sorted_data=SortedGfemData(
                            vbd=self.__vbd,
                            prepared_data=GfemDataFrame(
                                parser=self.__five_year_parser_vbd,
                                file_path=self.__path_str)))

                    self.__five_year_scenarios_vbd[month]['Data'] = self.__five_year_scenarios_vbd[month][
                        'RegressionScenario'].scenarios()
                    self.__five_year_scenarios_vbd[month]['DataframeList'] = self.__five_year_scenarios_vbd[month][
                        'RegressionScenario'].dataframe

                self.__model['vbd']['scenario'] = self.__five_year_scenarios_vbd
            except KeyError as e:
                print(e)
                print('Ошибка свода в формате пятилетки ВБД')

            except:
                print('Ошибка свода в формате пятилетки ВБД')
        self.choose_month(value=self.months[self.index])

    def change_model(self):
        self.model_type = not self.model_type
        if not self.model_type:
            self.__five_year_scenarios = self.__model['origin']['scenario']
            self.max_value['ГПН'] = DataValue('176219')

        else:
            self.__five_year_scenarios = self.__model['vbd']['scenario']
            self.max_value['ГПН'] = DataValue('6217')

        self.choose_month(value=self.months[self.index])

    def __init_month_from_gfem(self, month: str):

        self.__data = self.__five_year_scenarios[month]['Data']
        self.__dataframe_list = self.__five_year_scenarios[month]['DataframeList']
        self.__solution = SolutionBalancer(dataframe_list=self.__dataframe_list,
                                           company_names=self.company_names_full)
        print('Прогноз показателей загружен')

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

        self.choose_month(value=self.months[self.index])
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
        if self.model_type:
            result_crude = np.array(self.forecast_list)[
                            0:len(self.__do_result_list())] + np.array(self.__do_result_list())
        else:
            result_crude = np.array(self.forecast_list)[
                       0:len(self.__do_result_list())] - np.array(self.__do_result_list())
        return result_crude

    def choose_month(self, value):
    #    self.control_option = False
        if self.__five_year_format:
            try:
              self.__init_month_from_gfem(month=value)
            except:
               print('Ошибка чтения данных для выбранного месяца, используются данные свода')
               self.__dataframe_list = self.__init_dataframe_list
               self.__data = self.__init_data

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
        self.__solution.export_overal_results(path=path, solution_index=j, month=self.__constraints.months[self.index], vbd = self.model_type)
