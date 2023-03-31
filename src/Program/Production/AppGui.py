import edifice
import numpy as np
import pandas as pd

from Program.Production.GfemScenarios import *

from edifice import Label,  Slider, Dropdown, View, CheckBox, Component, StateManager, Window, Button, ScrollView
from edifice.components.forms import FormDialog, Form
from edifice.components import plotting


class Application(Component):

    def __init__(self,
                 scenarios: RegressionScenarios,
                 path: str = None):

        self.scenarios = scenarios
        self.path = Path(path)
        super().__init__()

        self.base_crude = False
        self.condence = False
        self.joint_venture = True
        self.label_width = 200

        self.state = StateManager({
            "File": pathlib.Path(""),
        })

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

        self.sum_value = self.vostok_value + self.megion_value + self.messoyaha_value + self.nng_value + self.orenburg_value + self.hantos_value + self.yamal_value
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
        self.result_crude = np.zeros(17)
        self.control_option = True

    def initialization(self):
        data = self.scenarios.scenarios()
        self.constraints = Constraints(path=self.path)
        self.constraints.load_constraints()

        self.data = data
        self.company_names = self.scenarios.company_names.copy()

        self.min_full = 0
        self.max_full = data[0]['ГПН'][2]
    #    self.fcf_full = data[0]['ГПН'][0].predict(np.array(self.min_full).reshape(-1, 1))
        self.fcf_full = np.array(
                [0])
        self.min_jv = 0
        self.max_jv = data[1]['ГПН'][2]
     #   self.fcf_jv = data[1]['ГПН'][0].predict(np.array(self.min_jv).reshape(-1, 1))
        self.fcf_jv = np.array(
                [0])
        for name in self.company_names:
            self.min_value_full[name] = 0
            self.max_value_full[name] = data[0][name][2]
            self.fcf_value_full[name] = np.array(
                [0])
        for name in self.company_names:
            self.min_value_jv[name] = 0
            self.max_value_jv[name] = data[1][name][2]
            self.fcf_value_jv[name] = np.array(
                [0])
        self._choose_scenario()

        self.dataframe_list = self.scenarios.dataframe
        self.solution = SolutionBalancer(dataframe_list=self.dataframe_list,
                                         company_names=self.company_names)

    def _choose_scenario(self):

        self.joint_venture = not self.joint_venture
        do_value = self._do_value_list()
        if self.joint_venture:
            self.min_value = self.min_value_jv
            self.max_value = self.max_value_jv
            self.company_min = self.min_jv
            self.company_max = self.max_jv
            self.company_value = self.company_min
            self.fcf_value = self.fcf_value_jv
            for i in range(len(do_value)):
                do_value[i] = self.min_value_jv[self.company_names[i]]

        if not self.joint_venture:
            self.min_value = self.min_value_full
            self.max_value = self.max_value_full
            self.company_min = self.min_full
            self.company_max = self.max_full
            self.company_value = self.company_min
            self.fcf_value = self.fcf_value_full
            for i in range(len(do_value)):
                do_value[i] = self.min_value_full[self.company_names[i]]
        self.company_value = 0

    def plot(self, ax):
        x = np.linspace(0, self.company_max, 100)
        if self.joint_venture:
            j = 1
        else:
            j = 0
        y = self.data[j]['ГПН'][0].predict(x[:, np.newaxis])
        ax.plot(x, y)
        x2 = np.linspace(0, self.company_value, 100)
        y2 = self.data[j]['ГПН'][0].predict(x2[:, np.newaxis])
        ax.plot(x2, y2)

    def _do_value_list(self):
        return [self.vostok_value,
                self.megion_value,
                self.messoyaha_value,
                self.nng_value,
                self.orenburg_value,
                self.hantos_value,
                self.yamal_value]

    def _company_result_list(self):
        company_result_list = self.constraints.dataframe['ДО'].iloc[:17].to_list()
        return company_result_list

    def _do_result_list(self):
        return [self.vostok_value,
                self.megion_value,
                self.messoyaha_value,
                self.nng_value,
                self.orenburg_value,
                self.hantos_value,
                self.yamal_value,
                0,0,0,0,0,0,0,0,0,0]

    def _update_fcf(self):
        do_value = self._do_value_list()
        if self.joint_venture:
            j = 1
        else:
            j = 0

        for i in range(len(do_value)):
            if do_value[i] == 0:
                self.fcf_value[self.company_names[i]] = np.array([0])
            else:
                self.fcf_value[self.company_names[i]] = self.data[j][self.company_names[i]][0].predict(np.array(do_value[i]).reshape(-1, 1))
        if self.company_value == 0:
            self.company_fcf = np.array([0])
        else:
            self.company_fcf = np.array([0])

    def _set_value(self, value):
        self.control_option = True
        self.set_state(company_value=value)
        self._find_solution()

    def _choose_month(self, value):
        self.set_state(index=int(np.where(self.constraints.months == value)[0]))
        self._set_value(value=self.constraints.extract_value(index=int(np.where(self.constraints.months == value)[0])))
        self.set_state(index=int(np.where(self.constraints.months == value)[0]))
        self._set_value(value=self.constraints.extract_value(index=int(np.where(self.constraints.months == value)[0])))
        self.sum_value = self.vostok_value + self.megion_value + self.messoyaha_value + self.nng_value + self.orenburg_value + self.hantos_value + self.yamal_value

    def _find_solution(self, company_name: str = 'All', company_value: float = 0.0):
        if self.joint_venture:
            j = 1
        else:
            j = 0
        if self.control_option:
            new_values = self.solution.result(crude_value=self.company_value,
                                              solution_index=j)
        else:
            new_values = self.solution.result(crude_value=self.company_value,
                                              solution_index=j,
                                              company_name=company_name,
                                              company_value=company_value)

        for i in range(len(new_values)):
            if self.max_value[self.company_names[i]] < new_values[i]:
                new_values[i] = self.max_value[self.company_names[i]]
            if self.min_value[self.company_names[i]] > new_values[i]:
                new_values[i] = self.min_value[self.company_names[i]]

        self.vostok_value = new_values[0]
        self.megion_value = new_values[1]
        self.messoyaha_value = new_values[2]
        self.nng_value = new_values[3]
        self.orenburg_value = new_values[4]
        self.hantos_value = new_values[5]
        self.yamal_value = new_values[6]
        self.sum_value = self.vostok_value + self.megion_value + self.messoyaha_value + self.nng_value + self.orenburg_value + self.hantos_value + self.yamal_value

        self.result_crude = np.array(self.constraints.extract_list(index=self.index))[0:len(self._do_result_list())] - np.array(self._do_result_list())

    def set_do_value(self, value, copmany: str):

        self.control_option = False

        if copmany == self.company_names[0]:
            self.set_state(vostok_value=value)
        if copmany == self.company_names[1]:
            self.set_state(megion_value=value)
        if copmany == self.company_names[2]:
            self.set_state(messoyaha_value=value)
        if copmany == self.company_names[3]:
            self.set_state(nng_value=value)
        if copmany == self.company_names[4]:
            self.set_state(orenburg_value=value)
        if copmany == self.company_names[5]:
            self.set_state(hantos_value=value)
        if copmany == self.company_names[6]:
            self.set_state(yamal_value=value)
        if copmany == self.company_names[0]:
            self.set_state(vostok_value=value)
        if copmany == self.company_names[1]:
            self.set_state(megion_value=value)
        if copmany == self.company_names[2]:
            self.set_state(messoyaha_value=value)
        if copmany == self.company_names[3]:
            self.set_state(nng_value=value)
        if copmany == self.company_names[4]:
            self.set_state(orenburg_value=value)
        if copmany == self.company_names[5]:
            self.set_state(hantos_value=value)
        if copmany == self.company_names[6]:
            self.set_state(yamal_value=value)
        self._find_solution(company_name=copmany, company_value=value)
        self.sum_value = self.vostok_value + self.megion_value + self.messoyaha_value + self.nng_value + self.orenburg_value + self.hantos_value + self.yamal_value



    def add_default_slider(self, name: str, value):
        return View(layout="row", )(
            Label(name, style=self.default_label(i=1),),
            Slider(value=value,
                   min_value=self.min_value[name],
                   max_value=self.max_value[name],
                   on_click=lambda value: self.control(),
                   on_change=lambda value: self.set_do_value(value=value, copmany=name)),
            Label(round(value, 1),
                  style=self.default_label(i=3)),
            Label(self.fcf_value[name].round()[0],
                  style=self.default_label(i=3))
            )

    def default_label(self, i: int):
        if i == 1:
            return {"width": self.label_width}
        if i == 2:
            return {"align": "center"}
        if i == 3:
            return {"width": self.label_width / 2, "margin": 5, "align": "center"}

    def add_divider(self, comp, comp2, comp3, comp4):

        return View(layout="row")\
            (View(layout="column")(
                comp,
                View(style={"height": 0, "border": "1px solid gray"})
                                    ),
            (View(layout="column")(
                comp2,
                View(style={"height": 0, "border": "1px solid gray"}))
            ),
            (View(layout="column")(
                comp3,
                View(style={"height": 0, "border": "1px solid gray"}))
            ),
            (View(layout="column")(
            comp4,
            View(style={"height": 0, "border": "1px solid gray"})))
        )

    def control(self):
        self.control_option = False

    def render(self):
        if self.control_option:
            self._find_solution()
        self._update_fcf()
        self.sum_value = self.vostok_value + self.megion_value + self.messoyaha_value + self.nng_value + self.orenburg_value + self.hantos_value + self.yamal_value
        self.sum_fcf = sum(self.fcf_value.values())

        return Window(title='Просмотрщик сценариев')(
            View(layout="column", style={"margin": 15, "font-weight": 1})
                (View(layout="row", )(
                    Label('Месяц прогноза', style=self.default_label(i=1), ),
                    Dropdown(selection='Месяц', options=self.constraints.months, on_select=lambda value: self._choose_month(value=value)),
                    Label('', style={"width": 30 }, ),
                    Label('Необходимо срезать добычи, т/сут.', style=self.default_label(i=1), ),
                    Label(round(self.constraints.extract_value(index=self.index)), style=self.default_label(i=1), )
                                    ),

                ScrollView(layout="column" , )
                    (View(layout="row", style={"border": "1px solid gray"})(
                                        Label('ДО'),
                                        Label('Прогноз добычи, т/сут.'),
                                        Label('Сокращение добычи, т/сут.'),
                                        Label('Итоговая добыча, т/сут.'),
                                        ),
                    *[self.add_divider(Label(name),
                                       Label(constraint, style=self.default_label(i=2)),
                                       Label(round(value), style=self.default_label(i=2)),
                                       Label(result.round(), style=self.default_label(i=2)),
                                       ) for name, constraint, value, result in zip(self._company_result_list(), self.constraints.extract_list(index=self.index),  self._do_result_list(), self.result_crude)],
                    (View(layout="row")),
                    ),

        View(layout="row")(Label('Итог'),
                           Label(round(self.constraints.extract_list(index=self.index).iloc[17]), style=self.default_label(i=2)),
                           Label(round(self.sum_value, 1), style=self.default_label(i=2)),
                           Label(self.result_crude.sum().round(), style=self.default_label(i=2)),
                           ),

        View(layout="row")(Label('Квота МЭ'),
                           Label(round(self.constraints.extract_list(index=self.index).iloc[18]),style=self.default_label(i=2)),
                           Label('', style=self.default_label(i=1)),
                           Label('', style=self.default_label(i=1)),
                           ),

        View(layout="row", )(
                    Label('ДО', style=self.default_label(i=1), ),
                    Label('Сокращение добычи', style={"width": 1.5 * self.label_width, }, ),
                    Label('т/сут.', style=self.default_label(i=3)),
                    Label('Потери FCF, тыс.руб.', style=self.default_label(i=3))
                ),
                View(layout="row", )(
                    Label('ГПН', style={"width": self.label_width, }, ),
                    Slider(value=self.company_value, min_value=self.company_min,
                           max_value=self.company_max,  # on_click=lambda value: self._find_solution(),
                           on_change=lambda value: self._set_value(value=value), ),
                    Label(round(self.company_value, 1),
                          style=self.default_label(i=3)),
                    Label(self.sum_fcf.round()[0],
                          style=self.default_label(i=3))
                ),

                *[self.add_default_slider(name, value) for name, value in zip(self.company_names, self._do_value_list())],

                View(layout="row")(
                    Label('', style={"width": self.label_width}),
                    Label('Сумма', style={"width": 1.5 * self.label_width, "align": "center"}, ),
                    Label(round(self.sum_value, 1), style=self.default_label(i=3)),
                    Label(self.sum_fcf.round()[0], style=self.default_label(i=3))
                ),
                View(layout="row")(
                View(layout="column", style={"height": 250})(
                  #  CheckBox(text='Базовая добыча', ),
                  #  CheckBox(text='ГТМ'),
                 #   CheckBox(text='Конденсат'),
                    CheckBox(text='Учет доли СП', checked=self.joint_venture,
                             on_change=lambda value: self._choose_scenario()),
                ),

                plotting.Figure(lambda ax: self.plot(ax))),

                View(layout="row")(
                    Form(self.state, ),
                    Button("Загрузить объекты в Excel", style={"width": self.label_width * 2}, on_click=lambda value: self.solution.export_results(path=self.state['File'])),
                ),
            )
        )

