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


        self.vostok_fcf = DataValue('0.0')
        self.megion_fcf = DataValue('0.0')
        self.messoyaha_fcf = DataValue('0.0')
        self.nng_fcf = DataValue('0.0')
        self.orenburg_fcf = DataValue('0.0')
        self.hantos_fcf = DataValue('0.0')
        self.yamal_fcf = DataValue('0.0')

        self.full_company_list = []
        self.forecast_list = []
        self.crude_list = []
        self.result_crude_list = []

        self.joint_venture = False

        self.__fcf_value_full = {}
        self.__fcf_value_jv = {}
        self.__fcf_full = 0
        self.__fcf_jv = 0
        self.__fcf_value = {}

        self.__constraints = None
        self.__data = None
        self.__company_names = None
        self.__solution = None
        self.__dataframe_list = None
        self.months = None
        self.__control_option = True


        self.__min_value_full = {}
        self.__max_value_full = {}

        self.__min_value_jv = {}
        self.__max_value_jv = {}

        self.__min_value = {}
        self.__max_value = {}
        self.__index = 0
        self.target = DataValue('0')


    def initializtion(self):
        self.__data = self.scenarios.scenarios()
        self.__constraints = Constraints(path=self.path)
        self.__constraints.load_constraints()

        self.__company_names = self.scenarios.company_names.copy()

        self.__min_full = 0
        self.__max_full = self.__data[0]['ГПН'][2]
        self.__fcf_full = np.array([0])

        self.__min_jv = 0
        self.__max_jv = self.__data[1]['ГПН'][2]
        self.__fcf_jv = np.array([0])

        for name in self.__company_names:
            self.__min_value_full[name] = 0
            self.__max_value_full[name] = self.__data[0][name][2]
            self.__fcf_value_full[name] = np.array([0])
            self.__min_value_jv[name] = 0
            self.__max_value_jv[name] = self.__data[1][name][2]
            self.__fcf_value_jv[name] = np.array([0])

        self.__choose_scenario()

        self.__dataframe_list = self.scenarios.dataframe
        self.__solution = SolutionBalancer(dataframe_list=self.__dataframe_list,
                                           company_names=self.__company_names)
        self.target = DataValue(str(self.__constraints.extract_value(index=self.__index)))
        self.months = self.__constraints.months

        self.full_company_list = self.__company_result_list()
        self.forecast_list = []
        self.crude_list = []
        self.result_crude_list = []


    def __company_result_list(self):
        company_result_list = self.__constraints.dataframe['ДО'].iloc[:23].to_list()
        return company_result_list

    def choose_month(self, value):

        self.index = int(np.where(self.__constraints.months == value)[0])
        val = self.__constraints.extract_value(index=int(np.where(self.__constraints.months == value)[0]))
        self.set_value(value=val)
        self.quota = round(self.__constraints.extract_list(index=self.index).iloc[21])

    def on_click(self):
        self.control_option = False

    def set_value(self, company_value):
        self.control_option = True

        new_crude_values = self._find_solution(target=value)




    def __update_values_for_view(self, values):


    def _find_solution(self, company_name: list = ['All'], company_value: list = [0.0], target: float = 0):

        self.last_target = target
        if self.joint_venture:
            j = 1
        else:
            j = 0
        if self.control_option:
            new_values = self.solution.result(crude_value=target,
                                              solution_index=j)
        else:
            new_values = self.solution.result(crude_value=target,
                                              solution_index=j,
                                              company_name=company_name,
                                              company_value=company_value)

        for i in range(len(new_values)):
            if self.max_value[self.company_names[i]] < new_values[i]:
                new_values[i] = self.max_value[self.company_names[i]]
            if self.min_value[self.company_names[i]] > new_values[i]:
                new_values[i] = self.min_value[self.company_names[i]]
        return new_values

    def __choose_scenario(self):

        self.joint_venture = not self.joint_venture

        if self.joint_venture:
            a = self.min_value_jv
            b = self.max_value_jv
            c = self.min_jv
            d = self.max_jv
            e = self.company_min
            f = self.fcf_value_jv
            for i in range(len(do_value)):
                do_value[i] = self.min_value_jv[self.company_names[i]]

        else:
            a = self.min_value_full
            b = self.max_value_full
            c = self.min_full
            d = self.max_full
            e = self.company_min
            f = self.fcf_value_full
            for i in range(len(do_value)):
                do_value[i] = self.min_value_full[self.company_names[i]]
        self.min_value = a
        self.max_value = b
        self.company_min = c
        self.company_max = d
        self.company_value = e
        self.fcf_value = f
        self.company_value = 0

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