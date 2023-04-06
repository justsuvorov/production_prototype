import edifice
import numpy as np
import pandas as pd
from copy import deepcopy, copy

from Program.Production.GfemScenarios import *

from edifice import Label,  Slider, Dropdown, View, CheckBox,TextInput,  Component, StateManager, Window, Button, ScrollView
from edifice.components.forms import FormDialog, Form
from edifice.components import plotting
from edifice import Timer


app_state = StateManager({
            'company_value': 0.0,
            'vostok_value': 0.0,
            'megion_value':  0.0,
            'messoyaha_value': 0.0,
            'nng_value': 0.0,
            'orenburg_value': 0.0,
            'hantos_value': 0.0,
            'yamal_value': 0.0,
            'sum_value': 0.0,
            "File": pathlib.Path(""),
        })

class Application(Component):

    def __init__(self,
                 scenarios: RegressionScenarios,
                 path: str = None):

        self.scenarios = scenarios
        self.path = Path(path)
        super().__init__()

        self.state = StateManager({
            "File": pathlib.Path(""),
        })

        self.joint_venture = True
        self.label_width = 200

        self.min_value_full = {}
        self.max_value_full = {}

        self.min_value_jv = {}
        self.max_value_jv = {}

        self.min_value = {}
        self.max_value = {}

        self.vostok_value = 0.0
        self.megion_value = 0.0
        self.messoyaha_value = 0.0
        self.nng_value = 0.0
        self.orenburg_value = 0.0
        self.hantos_value = 0.0
        self.yamal_value = 0.0

        self.vostok_value_lab = 0.0
        self.megion_value_lab = 0.0
        self.messoyaha_value_lab = 0.0
        self.nng_value_lab = 0.0
        self.orenburg_value_lab = 0.0
        self.hantos_value_lab = 0.0
        self.yamal_value_lab = 0.0

        #self.sum_value = self.vostok_value + self.megion_value + self.messoyaha_value + self.nng_value + self.orenburg_value + self.hantos_value + self.yamal_value
        self.sum_fcf = 0
        self.fcf_value_full = {}
        self.fcf_value_jv = {}
        self.fcf_full = 0
        self.fcf_jv = 0
        self.fcf_value = {}

        self.company_min = 0
        self.company_max = 0
        self.company_value = 0

        self.company_fcf = 0

        self.data = None

        self.company_names = []
        self.dataframe_list = None
        self.solution = None
        self.constraints = None
        self.index = 0
        self.result_crude = np.zeros(20)
        self.control_option = True

        self.last_company = 'All'
        self.last_company_value = 0.0
        self.label_sum = 0
        self.last_target = 0
        self.label_do = []

    def initialization(self):
        data = self.scenarios.scenarios()
        self.constraints = Constraints(path=self.path)
        self.constraints.load_constraints()

        self.data = data
        self.company_names = self.scenarios.company_names.copy()

        self.min_full = 0
        self.max_full = data[0]['ГПН'][2]
        self.fcf_full = np.array([0])

        self.min_jv = 0
        self.max_jv = data[1]['ГПН'][2]
        self.fcf_jv = np.array([0])

        for name in self.company_names:
            self.min_value_full[name] = 0
            self.max_value_full[name] = data[0][name][2]
            self.fcf_value_full[name] = np.array([0])
            self.min_value_jv[name] = 0
            self.max_value_jv[name] = data[1][name][2]
            self.fcf_value_jv[name] = np.array([0])

        self._choose_scenario()

        self.dataframe_list = self.scenarios.dataframe
        self.solution = SolutionBalancer(dataframe_list=self.dataframe_list,
                                         company_names=self.company_names)
        self.label_do = self._do_result_list().copy()

    def _choose_scenario(self):

        self.joint_venture = not self.joint_venture
        do_value = self._do_value_list()
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

    def plot(self, ax):
        if self.joint_venture:
            j = 1
        else:
            j = 0
        if self.last_company =='All':
            x = np.linspace(0, self.company_max, 100)
            y = self.data[j]['ГПН'][0].predict(x[:, np.newaxis])
            ax.plot(x, y)
            x2 = np.linspace(0, self.company_value, 100)
            y2 = self.data[j]['ГПН'][0].predict(x2[:, np.newaxis])
            ax.plot(x2, y2)
        else:
            x = np.linspace(0, self.max_value[self.last_company], 100)
            y = self.data[j][self.last_company][0].predict(x[:, np.newaxis])
            ax.plot(x, y)
            x2 = np.linspace(0, self.last_company_value, 100)
            y2 = self.data[j][self.last_company][0].predict(x2[:, np.newaxis])
            ax.plot(x2, y2)

    def _do_value_list(self):
        a = [self.vostok_value,
             self.megion_value,
             self.messoyaha_value,
             self.nng_value,
             self.orenburg_value,
             self.hantos_value,
             self.yamal_value]
        return a.copy()

    def _company_result_list(self):
        company_result_list = self.constraints.dataframe['ДО'].iloc[:23].to_list()
        return company_result_list

    def _do_result_list(self):
        result = [self.vostok_value_lab,
                self.megion_value_lab,
                self.messoyaha_value_lab,
                self.nng_value_lab,
                self.orenburg_value_lab,
                self.hantos_value_lab,
                self.yamal_value_lab]

        return [0,
                result[0],0,0,0,
                result[2],
                result[4],0,
                result[1],
                result[5],
                result[6],
                result[3],
                0,0,0,0,0,0,0,0,]

    def _update_fcf(self):
        do_value = self._do_value_list().copy()
        fcf = {}
        if self.joint_venture:
            j = 1
        else:
            j = 0

        for i in range(len(do_value)):
            if do_value[i] == 0:
                fcf[self.company_names[i]] = np.array([0])
            else:
                fcf[self.company_names[i]] = self.data[j][self.company_names[i]][0].predict(np.array(do_value[i]).reshape(-1, 1))
        if self.company_value == 0:
            self.company_fcf = np.array([0])
        else:
            self.company_fcf = np.array([0])
        self.set_state(fcf_value=fcf)

        self.set_state(sum_fcf=np.sum(list(fcf.values())).round())

    def _set_value(self, value):
        self.control_option = True
        self.last_company = 'All'
        self.last_company_value = 0
        self.set_state(company_value=value)
        new_values = self._find_solution(target=value)
        i = 0

        for name in self.company_names:
            self.set_do_value(value=new_values[i], copmany=name)
            i = i + 1
        self.set_state(label_sum=np.sum(new_values))

    def _choose_month(self, value):
        self.set_state(index=int(np.where(self.constraints.months == value)[0]))
        val = self.constraints.extract_value(index=int(np.where(self.constraints.months == value)[0]))
        self._set_value(value=val)

    def _find_solution(self, company_name: str = 'All', company_value: float = 0.0, target: float = 0):

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

    def set_do_value(self, value, copmany: str):
        if not isinstance(value, float): value = self.last_company_value
        self.control_option = False
        if value > self.company_value:
            value = self.company_value
        if copmany == self.company_names[0]:
            self.set_state(vostok_value=value)
            self.set_state(vostok_value_lab=value)
        if copmany == self.company_names[1]:
            self.set_state(megion_value=value)
            self.set_state(megion_value_lab=value)
        if copmany == self.company_names[2]:
            self.set_state(messoyaha_value=value)
            self.set_state(messoyaha_value_lab=value)
        if copmany == self.company_names[3]:
            self.set_state(nng_value=value)
            self.set_state(nng_value_lab=value)
        if copmany == self.company_names[4]:
            self.set_state(orenburg_value=value)
            self.set_state(orenburg_value_lab=value)
        if copmany == self.company_names[5]:
            self.set_state(hantos_value=value)
            self.set_state(hantos_value_lab=value)
        if copmany == self.company_names[6]:
            self.set_state(yamal_value=value)
            self.set_state(yamal_value_lab=value)
        self.label_sum = round(sum(self._do_result_list()))
        self.set_state(label_do=self._do_result_list())
        self.result_crude = np.array(self.constraints.extract_list(index=self.index))[
                            0:len(self._do_result_list())] - np.array(self._do_result_list())
        self._update_fcf()

    def _click(self,):
        new_values = self._find_solution(target=self.last_target,
                                         company_name=self.last_company,
                                         company_value=self.last_company_value)
        i = 0
        for name in self.company_names:
            self.set_do_value(value=new_values[i], copmany=name)
            i = i + 1
        self.set_state(label_sum=np.sum(new_values))

    def add_default_slider(self, name: str, value):
        return View(layout="row", )(
            Label(name, style=self.default_label(i=1),),
            Slider(value=value,
                   min_value=self.min_value[name],
                   max_value=self.max_value[name],
                   on_mouse_up=lambda value1: self.control(copmany=name, value=value),
                   on_mouse_down=lambda value1: self.control(copmany=name, value=value),
                   on_change=lambda value1: self.set_do_value(value=value1, copmany=name)),
            TextInput(text=str(round(value, 1)),
                      on_click=lambda value1: self.control(copmany=name, value=value),
                  #    on_change=lambda value1: self.set_do_value(value=float(value1), copmany=name),
                      on_edit_finish= lambda: self._click(),
                      style=self.default_label(i=6)),
          #  TextInput(round(float(value), 1), on_change=lambda value: self.set_do_value(value=float(value), copmany=name)),
            Label(self.fcf_value[name].round()[0],
                  style=self.default_label(i=3))
            )

    def default_label(self, i: int):
        if i == 1: #
            return {"width": self.label_width}
        if i == 2: # верхняя таблица
            return {"align": "center", 'height': 30}
        if i == 3:
            return {"width": self.label_width / 2, "margin": 5, "align": "center"}
        if i == 4:
            return {"width": 200, "margin": 5, "align": "right"}
        if i == 5:
            return {"align": "center", 'height': 30, 'font-weight': 10}
        if i == 6:
            return {"width": self.label_width / 2, "margin": 5, "align": "center", "border": "0px"}

    def add_divider(self, comp, comp2, comp3, comp4):

        return View(layout="row", style = {'background-color': 'white'})\
            (View(layout="column",style = {'background-color': 'white'})(
                comp,
                View(style={"height": 0, "border": "1px solid gray", })
                                    ),
            (View(layout="column")(
                comp2,
                View(style={"height": 0, "border": "1px solid gray", }))
            ),
            (View(layout="column")(
                comp3,
                View(style={"height": 0, "border": "1px solid gray"}))
            ),
            (View(layout="column")(
            comp4,
            View(style={"height": 0, "border": "1px solid gray", })))
        )

    def control(self, copmany, value):
        self.control_option = False
        self.last_company = copmany
        self.last_company_value = value

    def update_parameters(self):

        result_crude = copy(self.result_crude)
        do_result = self._do_value_list()
        company_value = copy(self.company_value)

        return do_result, result_crude, company_value

    def application(self, do_result,  result_crude, company_value):
        return Window(title='Просмотрщик сценариев', )(
            View(layout="column",style={'background-color': 'white', "margin": 10, "font-weight": 1},)#""" style={"margin": 10, "font-weight": 1},"""
                (View(layout="row", style={"margin": 10, "font-weight": 1})(
                Label('Месяц прогноза', style=self.default_label(i=1), ),
                Dropdown(selection='Месяц', options=self.constraints.months,
                         on_select=lambda value: self._choose_month(value=value), ),
                Label('', style={"width": 30}, ),
                Label('Необходимо срезать добычи, т/сут.', style=self.default_label(i=1), ),
                Label(round(self.constraints.extract_value(index=self.index)), style=self.default_label(i=1), )
            ),

                ScrollView(layout="column")
                    (View(layout="row")(
                        self.add_divider(Label('ДО', style=self.default_label(i=2)),
                                         Label('Прогноз добычи, т/сут.', style=self.default_label(i=2)),
                                         Label('Сокращение добычи, т/сут.', style=self.default_label(i=2)),
                                         Label('Итоговая добыча, т/сут.', style=self.default_label(i=2)),),
                                        ),
                        *[self.add_divider(Label(name),
                                         Label(constraint, style=self.default_label(i=2)),
                                         Label(round(value), style=self.default_label(i=2)),
                                         Label(result.round(), style=self.default_label(i=2)),
                                          ) for name, constraint, value, result in zip(self._company_result_list(),
                                                                                    self.constraints.extract_list(
                                                                                        index=self.index), self.label_do,
                                                                                    result_crude)],
                      #  (View(layout="row")(self.add_divider(Label(''),Label(''),Label(''),Label('')),)),
                ),
                View(layout='column', style={"margin": 5, "font-weight": 1})(
                View(layout="row")(Label('Итог'),
                                   Label(round(self.constraints.extract_list(index=self.index).iloc[20]),
                                         style=self.default_label(i=5)),
                                   Label(round(self.label_sum), style=self.default_label(i=5)),
                                   Label(result_crude.sum().round(), style=self.default_label(i=5)),
                                   ),

                View(layout="row", style={})(self.add_divider(Label('Квота МЭ'),
                                   Label(round(self.constraints.extract_list(index=self.index).iloc[21]),
                                         style=self.default_label(i=5)),
                                   Label('', ),
                                   Label('',),
                                   )
                                   )),

                View(layout="row", )(
                    Label('ДО', style=self.default_label(i=1), ),
                    Label('Сокращение добычи', style={"width": 1.5 * self.label_width, }, ),
                    Button('Расчет', on_click=lambda a: self._click()),
                    Label('т/сут.', style=self.default_label(i=3)),
                    Label('Потери FCF, млн.руб.', style=self.default_label(i=3)),

                ),
                View(layout="row", )(
                    Label('ГПН', style={"width": self.label_width, }, ),
                    Slider(value=company_value, min_value=self.company_min,
                           max_value=self.company_max,  # on_click=lambda value: self._find_solution(),
                           on_change=lambda value1: self._set_value(value=value1), ),
                    Label(round(company_value, 1),
                          style=self.default_label(i=3)),
                    Label(self.sum_fcf,
                          style=self.default_label(i=3))
                ),
                View(layout="row", )(
                    Label('', style={"width": self.label_width, }, ),


                ),

                *[self.add_default_slider(name, value) for name, value in zip(self.company_names, do_result)],


                View(layout="row")(
                    Label('', ),
                    Label('Сумма', style={"width": 450, "align": "right"}, ),
                    Label(round(self.label_sum), style=self.default_label(i=3)),
                    Label(self.sum_fcf, style=self.default_label(i=3), )
                ),
                View(layout="row", )(
              #      View(layout="column", style={"height": 190})(
                        #  CheckBox(text='Базовая добыча', ),
                        #  CheckBox(text='ГТМ'),
                        #   CheckBox(text='Конденсат'),
                        CheckBox(text='Учет доли СП', checked=self.joint_venture,
                                 on_change=lambda value: self._choose_scenario(), style={"width": self.label_width / 1.5, "align": "center", "height": 190, }),
                        plotting.Figure(lambda ax: self.plot(ax)),  # ),
                    ),

                View(layout="row")(
                    Form(self.state, ),
                    Button("Загрузить объекты в Excel", style={"width": self.label_width * 2},
                           on_click=lambda value: self.solution.export_results(path=self.state['File'])),
                ),
            )
        )

    def render(self):
        do_result, result_crude, company_value = self.update_parameters()
        window = self.application(do_result, result_crude, company_value)

        return window

