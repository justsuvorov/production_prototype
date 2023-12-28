from Program.GUI.data_value import DataValue
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