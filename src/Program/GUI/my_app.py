from edifice import Label,  Slider, Dropdown, View, CheckBox,TextInput,  Component, StateManager, Window, Button, ScrollView
from edifice.components.forms import FormDialog, Form
from edifice.components import plotting
from data_model import DataModel
from data_value import DataValue
from Program.GUI.components import default_label, DefaultSlider, add_divider, DefaultDropdown


class MyApplication(Component):
    def __init__(self,
                 data_model: DataModel,
                 ):
        super().__init__()
        self.__model = data_model

    def __on_dropdown_select(self, value):
        self.__model.choose_month(value)
        self.set_state()

    def __on_gpn_changed(self, value):
        self.__model.set_value(value)
        self.set_state()


    def render(self):
        Window(title='Просмотрщик сценариев', )(
            View(layout="column", style={'background-color': 'white', "margin": 10,
                                         "font-weight": 1}, )  # """ style={"margin": 10, "font-weight": 1},"""
                (DefaultDropdown(value=self.__model.target,
                                 options=self.__model.months,
                                 onSelect=self.__on_dropdown_select),
            ),

                ScrollView(layout="column")
                    (View(layout="row")(
                    add_divider(Label('ДО', style=default_label(i=2)),
                                     Label('Прогноз добычи, т/сут.', style=default_label(i=2)),
                                     Label('Сокращение добычи, т/сут.', style=default_label(i=2)),
                                     Label('Итоговая добыча, т/сут.', style=default_label(i=2)), ),
                ),
                    *[add_divider(Label(name),
                                  Label(constraint, style=default_label(i=2)),
                                  Label(round(value), style=default_label(i=2)),
                                  Label(result.round(), style=default_label(i=2)),
                                  ) for name, constraint, value, result in zip(self.__model.full_company_list,
                                                                               self.__model.forecast_list,
                                                                               self.__model.crude_list,
                                                                               self.__model.result_crude_list)],

                ),
                View(layout='column', style={"margin": 5, "font-weight": 1})(
                    View(layout="row")(Label('Итог'),
                                       Label(self.__model.forecast_sum.toStr,
                                             style=default_label(i=5)),
                                       Label(self.__model.crude_sum.toStr, style=default_label(i=5)),
                                       Label(self.__model.result_crude_sum.toStr, style=default_label(i=5)),
                                       ),

                    View(layout="row", style={})(add_divider(Label('Квота МЭ'),
                                                                  Label(self.__model.quota,
                                                                        style=default_label(i=5)),
                                                                  Label('', ),
                                                                  Label('', ),
                                                                  )
                                                 )),

                View(layout="row", )(
                    Label('ДО', style=default_label(i=1), ),
                    Label('Сокращение добычи', style={"width": 1.5 * 200, }, ),
                    Button('Расчет', on_click= self.button_click),
                    Label('т/сут.', style=default_label(i=3)),
                    Label('Потери FCF, млн.руб.', style=default_label(i=3)),

                ),
                View(layout="row", )(
                    DefaultSlider(value=self.__model.company_value,
                                  fcf_value=self.__model.fcf_value,
                                  label='ГПН',
                                  min_value=self.__model.company_min,
                                  max_value=self.__model.company_max,
                                  onChanged=self.__on_gpn_changed),


                ),


                *[self.add_default_slider(name, value) for name, value in zip(self.company_names, do_result)],

                View(layout="row")(
                    Label('', ),
                    Label('Сумма', style={"width": 450, "align": "right"}, ),
                    Label(round(self.label_sum), style=self.default_label(i=3)),
                    Label(self.sum_fcf, style=self.default_label(i=3), )
                ),
                View(layout="row", )(
                    CheckBox(text='Учет доли СП', checked=self.joint_venture,
                             on_change=self._choose_scenario,
                             style={"width": self.label_width / 1.5, "align": "center", "height": 190, }),
                    plotting.Figure(lambda ax: self.plot(ax)),  # ),
                ),

                View(layout="row")(
                    Form(self.state, ),
                    Button("Загрузить объекты в Excel", style={"width": 200 * 2},
                           on_click=lambda value: self.solution.export_results(path=self.state['File'])),
                ),
            )
        )






class MyApp(Component):
    def __init__(self,
                 dataModel: DataModel,
                 ):
        super().__init__()
        self.__model = dataModel
        self.__rendered = 0

    def render(self):
        self.__rendered += 1
        print(f"rendered: {self.__rendered}")
        return View(layout="column")(
            MyEditField(
                label="Text input value 1:",
                value=self.__model.value1,
                onChanged=self.__onValue1Changed
            ),
            MyEditField(
                label="Text input value 2:",
                value=self.__model.value2,
                onChanged=self.__onValue2Changed
            ),
            MyEditField(
                label="Text input value 3:",
                value=self.__model.value3,
                onChanged=self.__onValue3Changed
            ),
            Button(
                title="solve",
                on_click=self.__onSolveButtonClicked
            )
        )

    def __onSolveButtonClicked(self):
        self.__model.__doMath1()

    def __onValue1Changed(self, value):
        print(f'new value: {value}')
        self.__model.changeValue1(value)
        self.set_state()

    def __onValue2Changed(self, value):
        print(f'new value: {value}')
        self.__model.changeValue2(value)
        self.set_state()

    def __onValue3Changed(self, value):
        print(f'new value: {value}')
        self.__model.changeValue3(value)
        self.set_state()