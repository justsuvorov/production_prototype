from Program.GUI.data_value import DataValue

import numpy as np
import pandas as pd
from copy import deepcopy, copy
from typing import Callable

from Program.Production.GfemScenarios import *

from edifice import Label,  Slider, Dropdown, View, CheckBox,TextInput,  Component, StateManager, Window, Button, ScrollView
from edifice.components.forms import FormDialog, Form
from edifice.components import plotting
from edifice import Timer

class DataModel:
    def __init__(self,
                 scenarios: RegressionScenarios,
                 path: str = None,
            ) -> None:

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


    def initializtion(self):
        self.__data = self.scenarios.scenarios()
        self.__constraints = Constraints(path=self.path)
        self.__constraints.load_constraints()

        self.company_names = self.scenarios.company_names.copy()

        self.__min_value_full['ГПН'] = DataValue(str(0))
        self.__max_value_full['ГПН'] = DataValue(str(self.__data[0]['ГПН'][2]))
        self.__min_value_jv['ГПН'] = DataValue(str(0))
        self.__max_value_jv['ГПН'] = DataValue(str(self.__data[1]['ГПН'][2]))

        for name in self.company_names:
            self.__min_value_full[name] = DataValue(str(0))
            self.__max_value_full[name] = DataValue(str(self.__data[0][name][2]))

            self.__min_value_jv[name] = DataValue(str(0))
            self.__max_value_jv[name] = DataValue(str(self.__data[1][name][2]))

        self.__dataframe_list = self.scenarios.dataframe
        self.__solution = SolutionBalancer(dataframe_list=self.__dataframe_list,
                                           company_names=self.company_names)
        self.target = DataValue(str(self.__constraints.extract_value(index=self.index)))
        self.months = self.__constraints.months

        self.full_company_list = self.__company_result_list()

        self.forecast_list = self.__constraints.extract_list(index=self.index)

        self.crude_list = self.__do_result_list()
        self.result_crude_list = self.__result_crude_list()

        self.choose_scenario()


    def choose_scenario(self):

        self.joint_venture = not self.joint_venture

        if self.joint_venture:
            self.min_value = self.__min_value_jv
            self.max_value = self.__max_value_jv

        else:
            self.min_value = self.__min_value_full
            self.max_value = self.__max_value_full

    def __company_result_list(self):
        company_result_list = self.__constraints.dataframe['ДО'].iloc[:23].to_list()
        return company_result_list

    def __do_result_list(self):
        result = [self.vostok_value.toFloat,
                self.megion_value.toFloat,
                self.messoyaha_value.toFloat,
                self.nng_value.toFloat,
                self.orenburg_value.toFloat,
                self.hantos_value.toFloat,
                self.yamal_value.toFloat]

        return [0,
                result[0],0,0,0,
                result[2],
                result[4],0,
                result[1],
                result[5],
                result[6],
                result[3],
                0,0,0,0,0,0,0,0,]

    def __result_crude_list(self):
        result_crude = np.array(self.forecast_list)[
                        0:len(self.__do_result_list())] - np.array(self.__do_result_list())
        return result_crude


    def choose_month(self, value):
    #    self.control_option = False
        self.index = int(np.where(self.__constraints.months == value)[0])
        val = self.__constraints.extract_value(index=int(np.where(self.__constraints.months == value)[0]))
        self.forecast_list = self.__constraints.extract_list(index=self.index)
        self.target.update(val)
        self.forecast_sum.update(self.__constraints.extract_list(index=self.index)[20])
        self.set_value(company_value=val)
        new_values = self._find_solution(target=val)
        self.__update_values_for_view(new_values)
        self.result_crude_list = self.__result_crude_list()
        self.result_crude_sum.update(sum(self.result_crude_list))
        self.quota.update(self.__constraints.extract_list(index=self.index).iloc[21])

    def on_click(self):
        self.__control_option = False

    def set_value(self, company_value):
  #      self.control_option = True
        self.__control_option = True
        self.company_value.update(company_value)
      #  new_crude_values = self._find_solution(target=company_value)
    #    self.__update_crude_values_for_view(values=new_crude_values)

    def on_gpn_change(self, company_value):
        self.set_value(company_value)
        new_values = self._find_solution(target=company_value)
        self.__update_values_for_view(new_values)
    #    self.result_crude_list = self.__result_crude_list()
    #    self.result_crude_sum.update(sum(self.result_crude_list))
     #   self.quota.update(self.__constraints.extract_list(index=self.index).iloc[21])

    def set_vostok_value(self, value):
        self.vostok_value.update(value)
        self.vostok_fcf.update(self._update_company_fcf(value, i=0))

    def set_megion_value(self, value):
        self.megion_value.update(value)
        self.megion_fcf.update(self._update_company_fcf(value, i=1))

    def set_messoyaha_value(self, value):
        self.messoyaha_value.update(value)
        self.messoyaha_fcf.update(self._update_company_fcf(value, i=2))

    def set_nng_value(self, value):
        self.nng_value.update(value)
        self.nng_fcf.update(self._update_company_fcf(value, i=3))

    def set_orenburg_value(self, value):
        self.orenburg_value.update(value)
        self.orenburg_fcf.update(self._update_company_fcf(value, i=4))

    def set_hantos_value(self, value):
        self.hantos_value.update(value)
        self.hantos_fcf.update(self._update_company_fcf(value, i=5))

    def set_yamal_value(self, value):
        self.yamal_value.update(value)
        self.yamal_fcf.update(self._update_company_fcf(value, i=6))


    def __update_values_for_view(self, values):

        self.crude_sum.update(sum(values))
        self.vostok_value.update(values[0])
        self.megion_value.update(values[1])
        self.messoyaha_value.update(values[2])
        self.nng_value.update(values[3])
        self.orenburg_value.update(values[4])
        self.hantos_value.update(values[5])
        self.yamal_value.update(values[6])

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
                fcf[i] = self.__data[j][self.company_names[i]][0].predict(np.array(values[i]).reshape(-1, 1))
        if self.company_value.toFloat == 0:
            self.company_fcf = DataValue('0')
        return fcf

    def _find_solution(self, company_name: list = ['All'], company_value: list = [0.0], target: float = 0):

        self.last_target = target
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
            if self.max_value[self.company_names[i]].toFloat < new_values[i]:
                new_values[i] = self.max_value[self.company_names[i]].toFloat
            if self.min_value[self.company_names[i]].toFloat > new_values[i]:
                new_values[i] = self.min_value[self.company_names[i]].toFloat
        return new_values


"""
    def changeValue1(self, value):
        self.value1.update(value)
        self.__doMath1()

    def changeValue2(self, value):
        self.value2.update(value)
        self.__doMath1()

    def changeValue3(self, value):
        self.value3.update(value)
        self.__doMath3()

    def __doMath1(self):
        value1 = self.value1.toFloat
        value2 = self.value2.toFloat
        # for i in range(1000000000000):
        #     value3 = 0.001 * (value1 + value2)
        value3 = 0.001 * (value1 + value2)
        self.__updateValuesForView(value1, value2, value3)


    def __doMath3(self):
        value3 = self.value3.toFloat
        value1 = value3 / 2
        value2 = value3 / 2
        self.__updateValuesForView(value1, value2, value3)


    def __updateValuesForView(self, value1, value2, value3):
        self.value1.update(value1)
        self.value2.update(value2)
        self.value3.update(value3)
"""

