import os

from edifice import Label,  Slider, Dropdown, View, CheckBox,TextInput,  Component, StateManager, Window, Button, ScrollView
from edifice.components.forms import FormDialog, Form
from edifice.components import plotting
from Program.GUI.data_model import DataModel, DataModelMonitoring
from Program.GUI.data_value import DataValue
from Program.GUI.components import default_label, DefaultSlider, add_divider, DefaultDropdown
import pathlib


class MyApplicationSixMonths(Component):
    def __init__(self,
                 data_model: DataModel,
                 result_path = None
                 ):
        super().__init__()
        self.__enableOnChangeCalback = True
        self.__model = data_model
        self.state = StateManager({
            "File": pathlib.Path(""),
        })
        self.result_path = result_path +'\Results.xlsx'

    def __on_dropdown_select(self, value):
        self.__model.choose_month(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_gpn_changed(self, value):
        self.__model.on_gpn_change(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_vostok_changed(self, value):
        self.__model.set_vostok_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_megion_changed(self, value):
        self.__model.set_megion_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_messoyaha_changed(self, value):
        self.__model.set_messoyaha_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_nng_changed(self, value):
        self.__model.set_nng_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_orenburg_changed(self, value):
        self.__model.set_orenburg_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_hantos_changed(self, value):
        self.__model.set_hantos_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_yamal_changed(self, value):
        self.__model.set_yamal_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_polar_changed(self, value):
        self.__model.set_polar_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_shelf_changed(self, value):
        self.__model.set_shelf_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_meretoyaha_changed(self, value):
        self.__model.set_meretoyaha_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_spd_changed(self, value):
        self.__model.set_spd_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_palyan_changed(self, value):
        self.__model.set_palyan_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_angara_changed(self, value):
        self.__model.set_angara_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_arctic_changed(self, value):
        self.__model.set_arctic_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_checkbox_changed(self,value ):
        self.__model.choose_scenario()
        self.__enableOnChangeCalback = False
     #   self.set_state()
        self.__enableOnChangeCalback = True

    def __onSaveButtonClick(self, value):
        if self.state['File'] ==pathlib.Path(""):
            path = pathlib.Path(self.result_path)
        else:
            path = self.state['File']
        self.__model.save_results(path=path)
        os.startfile(path)
        self.__enableOnChangeCalback = False
       # self.set_state()
        self.__enableOnChangeCalback = True

    def __on_Reset_click_button(self, value):
        self.__model.reset_results()
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def render(self):

        return Window(title='Просмотрщик сценариев', )(
                View(layout="column", style={'background-color': 'white', "margin": 10,
                                             "font-weight": 1},)  # """ style={"margin": 10, "font-weight": 1},"""
                    (
                    DefaultDropdown(value=self.__model.target,
                                    options=self.__model.months,
                                    onSelect=self.__on_dropdown_select if self.__enableOnChangeCalback else None),


                    ScrollView(layout="column")
                        (View(layout="row")(
                        add_divider(Label('ДО', style=default_label(i=2)),
                                    Label('Прогноз добычи, т/сут.', style=default_label(i=2)),
                                    Label('Сокращение добычи, т/сут.', style=default_label(i=2)),
                                    Label('Итоговая добыча, т/сут.', style=default_label(i=2)), ),
                                            ),

                   *[add_divider(Label(name),
                                  Label(constraint, style=default_label(i=2)),
                                  Label(value, style=default_label(i=2)),
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
                                                                      Label(self.__model.quota.toStr,
                                                                            style=default_label(i=5)),
                                                                      Label('', ),
                                                                      Label('', ),
                                                                      )
                                                     ),


                        View(layout="row", )(
                            Label('ДО', style=default_label(i=1), ),
                            Label('Сокращение добычи', style={"width": 1.5 * 200, }, ),
                            Button('Сбросить настройки', on_click=self.__on_Reset_click_button),
                            Label('т/сут.', style=default_label(i=3)),
                            Label('Потери FCF, млн.руб.', style=default_label(i=3)),

                                            ),

                        DefaultSlider(value=self.__model.company_value,
                                      fcf_value=self.__model.fcf_sum,
                                      label='ГПН',
                                      min_value=self.__model.min_value['ГПН'],
                                      max_value=self.__model.max_value['ГПН'],
                                      onChanged=self.__on_gpn_changed if self.__enableOnChangeCalback else None,

                                      ),


                        Label("", style={"width": 200, "align": 'center'}, ),



                        DefaultSlider(value=self.__model.vostok_value,
                                      fcf_value=self.__model.vostok_fcf,
                                      label=self.__model.company_names[0],
                                      min_value=self.__model.min_value['Восток'],
                                      max_value=self.__model.max_value['Восток'],
                                      onChanged=self.__on_vostok_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.megion_value,
                                      fcf_value=self.__model.megion_fcf,
                                      label=self.__model.company_names[1],
                                      min_value=self.__model.min_value['Мегионнефтегаз'],
                                      max_value=self.__model.max_value['Мегионнефтегаз'],
                                      onChanged=self.__on_megion_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.messoyaha_value,
                                      fcf_value=self.__model.messoyaha_fcf,
                                      label=self.__model.company_names[2],
                                      min_value=self.__model.min_value['Мессояханефтегаз'],
                                      max_value=self.__model.max_value['Мессояханефтегаз'],
                                      onChanged=self.__on_messoyaha_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.nng_value,
                                      fcf_value=self.__model.nng_fcf,
                                      label=self.__model.company_names[3],
                                      min_value=self.__model.min_value['ННГ'],
                                      max_value=self.__model.max_value['ННГ'],
                                      onChanged=self.__on_nng_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.orenburg_value,
                                      fcf_value=self.__model.orenburg_fcf,
                                      label=self.__model.company_names[4],
                                      min_value=self.__model.min_value['Оренбург'],
                                      max_value=self.__model.max_value['Оренбург'],
                                      onChanged=self.__on_orenburg_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.hantos_value,
                                      fcf_value=self.__model.hantos_fcf,
                                      label=self.__model.company_names[5],
                                      min_value=self.__model.min_value['Хантос'],
                                      max_value=self.__model.max_value['Хантос'],
                                      onChanged=self.__on_hantos_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.yamal_value,
                                      fcf_value=self.__model.yamal_fcf,
                                      label=self.__model.company_names[6],
                                      min_value=self.__model.min_value['Ямал'],
                                      max_value=self.__model.max_value['Ямал'],
                                      onChanged=self.__on_yamal_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.polar_value,
                                      fcf_value=self.__model.polar_fcf,
                                      label='Заполярье',
                                      min_value=self.__model.min_value['Заполярье'],
                                      max_value=self.__model.max_value['Заполярье'],
                                      onChanged=self.__on_polar_changed if self.__enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self.__model.shelf_value,
                                      fcf_value=self.__model.shelf_fcf,
                                      label='Шельф',
                                      min_value=self.__model.min_value['Шельф'],
                                      max_value=self.__model.max_value['Шельф'],
                                      onChanged=self.__on_shelf_changed if self.__enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self.__model.meretoyaha_value,
                                      fcf_value=self.__model.meretoyaha_fcf,
                                      label='Меретояханефтегаз',
                                      min_value=self.__model.min_value['Меретояханефтегаз'],
                                      max_value=self.__model.max_value['Меретояханефтегаз'],
                                      onChanged=self.__on_meretoyaha_changed if self.__enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self.__model.palyan_value,
                                      fcf_value=self.__model.palyan_fcf,
                                      label='Пальян',
                                      min_value=self.__model.min_value['Пальян'],
                                      max_value=self.__model.max_value['Пальян'],
                                      onChanged=self.__on_palyan_changed if self.__enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self.__model.spd_value,
                                      fcf_value=self.__model.spd_fcf,
                                      label='СПД',
                                      min_value=self.__model.min_value['СПД'],
                                      max_value=self.__model.max_value['СПД'],
                                      onChanged=self.__on_spd_changed if self.__enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self.__model.arctic_value,
                                      fcf_value=self.__model.arctic_fcf,
                                      label='Арктикгаз',
                                      min_value=self.__model.min_value['Арктикгаз'],
                                      max_value=self.__model.max_value['Арктикгаз'],
                                      onChanged=self.__on_arctic_changed if self.__enableOnChangeCalback else None,
                                      ),
                        DefaultSlider(value=self.__model.angara_value,
                                      fcf_value=self.__model.angara_fcf,
                                      label='Ангара',
                                      min_value=self.__model.min_value['Ангара'],
                                      max_value=self.__model.max_value['Ангара'],
                                      onChanged=self.__on_angara_changed if self.__enableOnChangeCalback else None,
                                      ),


                        View(layout="row")(
                    Label('', ),
                    Label('Сумма', style={"width": 450, "align": "right"}, ),
                    Label(round(self.__model.crude_sum.toFloat), style=default_label(i=3)),
                    Label(self.__model.fcf_sum.toStr, style=default_label(i=3), )
                ),



                        View(layout="row", )(
                            CheckBox(text='Учет доли СП', checked=self.__model.joint_venture,
                                     on_change=self.__on_checkbox_changed,
                                     style={"width": 200 / 1.5, "align": "left", "height": 50, }),
                          #  plotting.Figure(lambda ax: self.plot(ax)),  # ),
                        ),

                        View(layout="row")(
                            Form(self.state, ),
                            Button("Загрузить объекты в Excel", style={"width": 200 * 2},
                                   on_click=self.__onSaveButtonClick),)
                ),
            )
        )


class MyApplication(Component):
    def __init__(self,
                 data_model: DataModel,
                 result_path = None
                 ):
        super().__init__()
        self.__enableOnChangeCalback = True
        self.__refresh_plots = True
        self.__model = data_model
        self.state = StateManager({
            "File": pathlib.Path(""),
        })
        self.result_path = result_path +'\Results.xlsx'
        self.names = []

    def __on_dropdown_select(self, value):
        self.__model.choose_month(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_gpn_changed(self, value):
        self.__model.on_gpn_change(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_vostok_changed(self, value):
        self.__model.set_vostok_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_megion_changed(self, value):
        self.__model.set_megion_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_messoyaha_changed(self, value):
        self.__model.set_messoyaha_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_nng_changed(self, value):
        self.__model.set_nng_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_orenburg_changed(self, value):
        self.__model.set_orenburg_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_hantos_changed(self, value):
        self.__model.set_hantos_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_yamal_changed(self, value):
        self.__model.set_yamal_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_polar_changed(self, value):
        self.__model.set_polar_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_shelf_changed(self, value):
        self.__model.set_shelf_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_meretoyaha_changed(self, value):
        self.__model.set_meretoyaha_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_spd_changed(self, value):
        self.__model.set_spd_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_palyan_changed(self, value):
        self.__model.set_palyan_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_angara_changed(self, value):
        self.__model.set_angara_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_arctic_changed(self, value):
        self.__model.set_arctic_value(value)
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True

    def __on_checkbox_changed(self,value ):
        self.__model.choose_scenario()
        self.__enableOnChangeCalback = False
     #   self.set_state()
        self.__enableOnChangeCalback = True

    def __onSaveButtonClick(self, value):
        if self.state['File'] ==pathlib.Path(""):
            path = pathlib.Path(self.result_path)
        else:
            path = self.state['File']
        self.__model.save_results(path=path)
        os.startfile(path)
        self.__enableOnChangeCalback = False
       # self.set_state()
        self.__enableOnChangeCalback = True

    def __onSaveWholeTableButtonClick(self, value):
        if self.state['File'] == pathlib.Path(""):
            path = pathlib.Path(self.result_path)
        else:
            path = self.state['File']
        self.__model.save_overal_results(path=path)
        os.startfile(path)
        self.__enableOnChangeCalback = False
        # self.set_state()
        self.__enableOnChangeCalback = True

    def __on_Reset_click_button(self, value):
        self.__model.reset_results()
        self.__enableOnChangeCalback = False
        self.set_state()
        self.__enableOnChangeCalback = True


    def __plot_draw(self, ax):
        self.__refresh_plots = not self.__refresh_plots
        if self.__refresh_plots:
            self.set_state()

        x, y, x2, y2 = self.__model.plot_coordinates()
        colors = [
            # matplotlib named colors
            'cornflowerblue', 'tomato', 'orchid', 'gold',
            # any color using the color codes
            "#77BFE2", 'green', 'blue']
        i = 0
        labels = []

        for key in x:
            line = ax.plot(x[key], y[key], 5, color=colors[i])
            line[-1].set_label(key)
            i += 1

        ax.legend()

        for key in x:
            ax.plot(x2[key][-1], y2[key], color='#31363b', marker="o", markersize=8, label=None)
        ax.grid(True)
        ax.set(xlabel='Среднесуточная добыча, т/сут.', ylabel='FCF/Q, тыс.руб/т.',
               #  xlim=(10, 1.1 * self.__model.company_value.toFloat),
               xlim=(0, 7000),
               ylim=(0, 10,),
               title='Удельный FCF на тонну',
               )
    def __plot(self, ax):

        self.__plot_draw(ax)

    def __pie_plot(self, ax,):

        x2, values = self.__model.pie_plot_coordinates()
        x = x2.copy()
        values2 = values.copy()
        labels = ['Восток', 'Мегион', 'Мессояха', 'ННГ', 'Оренбург', 'Хантос', 'Ямал']
        labels2 = ['Восток', 'Мегион', 'Мессояха', 'ННГ', 'Оренбург', 'Хантос', 'Ямал']

        for i in range(len(x)):
            if (x[i]-0.001) < 0:
                x2.remove(x[i])
                labels2.remove(labels[i])
                values2.remove(values[i])
        i = 0
        labels_for_view = []

        for name in labels2:
            a = []
            a.append(name)
            a.append('('+str(round(values2[i], 1))+')')
            labels_for_view.append(' '.join(a))
            i += 1
        ax.set(title='Распределение квоты по ДО, т/сут.',

               )

      #  ax.set_facecolor('#31363b')
        ax.pie(x2, labels=labels_for_view, wedgeprops=dict(width=0.5), textprops={'fontsize': 8},
               colors=[
                   # matplotlib named colors
                    'cornflowerblue', 'tomato', 'gold', 'orchid', 'green',
                   # any color using the color codes
                   "#77BFE2", 'blue']
               )

     #   self.set_state()



    def render(self):

        return Window(title='Просмотрщик сценариев', )(
                View(layout="column", style={'background-color': '#002033', "margin": 10,
                                             "font-weight": 2, "font-size": 15},)  # """ style={"margin": 10, "font-weight": 1},"""
                    (
                    DefaultDropdown(value=self.__model.target,
                                     options=self.__model.months,
                                     onSelect=self.__on_dropdown_select if self.__enableOnChangeCalback else None),


                    ScrollView(layout="column",style = {'height': 120})
                        (View(layout="row", style={'background-color': '#002033', 'color': 'white' })(
                        add_divider(Label('ДО', style=default_label(i=2)),
                                    Label('Прогноз добычи, т/сут.', style=default_label(i=2)),
                                    Label('Сокращение добычи, т/сут.', style=default_label(i=2)),
                                    Label('Итоговая добыча, т/сут.', style=default_label(i=2)), ),
                                            ),

                   *[add_divider(Label(name, style={'background-color': '#002033', 'color': 'white' } ),
                                  Label(constraint, style=default_label(i=2)),
                                  Label(value, style=default_label(i=2)),
                                  Label(result.round(), style=default_label(i=2)),
                                  ) for name, constraint, value, result in zip(self.__model.full_company_list,
                                                                               self.__model.forecast_list,
                                                                               self.__model.crude_list,
                                                                               self.__model.result_crude_list)],

                    ),

                    View(layout='column', style={"margin": 1, "font-weight": 1})(
                        View(layout="row",  style={'height': 30})(Label('Итог', style=default_label(i=2)),
                                           Label(self.__model.forecast_sum.toStr,
                                                 style=default_label(i=5)),
                                           Label(self.__model.crude_sum.toStr, style=default_label(i=5)),
                                           Label(self.__model.result_crude_sum.toStr, style=default_label(i=5)),
                                         ),

                        View(layout="row",  style={'height': 30})(Label('Квота МЭ', style=default_label(i=2)),
                                                                      Label(self.__model.quota.toStr,
                                                                            style=default_label(i=5)),
                                                                      Label('',style=default_label(i=2) ),
                                                                      Label('', style=default_label(i=2)),

                                                     ),


                        View(layout="row",  style={'height': 30} )(
                            Label('ДО', style=default_label(i=1), ),
                            Label('Сокращение добычи', style={"width": 1.5 * 200, 'background-color': '#002033', 'color': 'white' }, ),
                            Button('Сбросить настройки', on_click=self.__on_Reset_click_button, style={'background-color': '#0091ff', 'color': 'white', 'height': 20} ),

                            Label('т/сут.', style=default_label(i=3)),
                            Label('Потери FCF, млн.руб.', style=default_label(i=3)),

                                            ),

                        DefaultSlider(value=self.__model.company_value,
                                      fcf_value=self.__model.fcf_sum,
                                      label='ГПН',
                                      min_value=self.__model.min_value['ГПН'],
                                      max_value=self.__model.max_value['ГПН'],
                                      onChanged=self.__on_gpn_changed if self.__enableOnChangeCalback else None,

                                      ),


                #        Label("", style={"width": 200, "align": 'center'}, ),

                        ScrollView(layout="column", style={'background-color': '#002033', 'color': 'white' , 'height': 170})(
                        DefaultSlider(value=self.__model.vostok_value,
                                      fcf_value=self.__model.vostok_fcf,
                                      label=self.__model.company_names[0],
                                      min_value=self.__model.min_value['Восток'],
                                      max_value=self.__model.max_value['Восток'],
                                      onChanged=self.__on_vostok_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.megion_value,
                                      fcf_value=self.__model.megion_fcf,
                                      label=self.__model.company_names[1],
                                      min_value=self.__model.min_value['Мегионнефтегаз'],
                                      max_value=self.__model.max_value['Мегионнефтегаз'],
                                      onChanged=self.__on_megion_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.messoyaha_value,
                                      fcf_value=self.__model.messoyaha_fcf,
                                      label=self.__model.company_names[2],
                                      min_value=self.__model.min_value['Мессояханефтегаз'],
                                      max_value=self.__model.max_value['Мессояханефтегаз'],
                                      onChanged=self.__on_messoyaha_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.nng_value,
                                      fcf_value=self.__model.nng_fcf,
                                      label=self.__model.company_names[3],
                                      min_value=self.__model.min_value['ННГ'],
                                      max_value=self.__model.max_value['ННГ'],
                                      onChanged=self.__on_nng_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.orenburg_value,
                                      fcf_value=self.__model.orenburg_fcf,
                                      label=self.__model.company_names[4],
                                      min_value=self.__model.min_value['Оренбург'],
                                      max_value=self.__model.max_value['Оренбург'],
                                      onChanged=self.__on_orenburg_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.hantos_value,
                                      fcf_value=self.__model.hantos_fcf,
                                      label=self.__model.company_names[5],
                                      min_value=self.__model.min_value['Хантос'],
                                      max_value=self.__model.max_value['Хантос'],
                                      onChanged=self.__on_hantos_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.yamal_value,
                                      fcf_value=self.__model.yamal_fcf,
                                      label=self.__model.company_names[6],
                                      min_value=self.__model.min_value['Ямал'],
                                      max_value=self.__model.max_value['Ямал'],
                                      onChanged=self.__on_yamal_changed if self.__enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self.__model.polar_value,
                                      fcf_value=self.__model.polar_fcf,
                                      label='Заполярье',
                                      min_value=self.__model.min_value['Заполярье'],
                                      max_value=self.__model.max_value['Заполярье'],
                                      onChanged=self.__on_polar_changed if self.__enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self.__model.shelf_value,
                                      fcf_value=self.__model.shelf_fcf,
                                      label='Шельф',
                                      min_value=self.__model.min_value['Шельф'],
                                      max_value=self.__model.max_value['Шельф'],
                                      onChanged=self.__on_shelf_changed if self.__enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self.__model.meretoyaha_value,
                                      fcf_value=self.__model.meretoyaha_fcf,
                                      label='Меретояханефтегаз',
                                      min_value=self.__model.min_value['Меретояханефтегаз'],
                                      max_value=self.__model.max_value['Меретояханефтегаз'],
                                      onChanged=self.__on_meretoyaha_changed if self.__enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self.__model.palyan_value,
                                      fcf_value=self.__model.palyan_fcf,
                                      label='Пальян',
                                      min_value=self.__model.min_value['Пальян'],
                                      max_value=self.__model.max_value['Пальян'],
                                      onChanged=self.__on_palyan_changed if self.__enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self.__model.spd_value,
                                      fcf_value=self.__model.spd_fcf,
                                      label='СПД',
                                      min_value=self.__model.min_value['СПД'],
                                      max_value=self.__model.max_value['СПД'],
                                      onChanged=self.__on_spd_changed if self.__enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self.__model.arctic_value,
                                      fcf_value=self.__model.arctic_fcf,
                                      label='Арктикгаз',
                                      min_value=self.__model.min_value['Арктикгаз'],
                                      max_value=self.__model.max_value['Арктикгаз'],
                                      onChanged=self.__on_arctic_changed if self.__enableOnChangeCalback else None,
                                      ),
                        DefaultSlider(value=self.__model.angara_value,
                                      fcf_value=self.__model.angara_fcf,
                                      label='Ангара',
                                      min_value=self.__model.min_value['Ангара'],
                                      max_value=self.__model.max_value['Ангара'],
                                      onChanged=self.__on_angara_changed if self.__enableOnChangeCalback else None,
                                      ),
                        ),


                        View(layout="row",  style={'height': 30})(
                            Label('', ),
                            Label('Сумма', style={"width": 450, "align": "right", 'background-color': '#002033', 'color': 'white' , }, ),
                            Label(round(self.__model.crude_sum.toFloat), style=default_label(i=3)),
                            Label(self.__model.fcf_sum.toStr, style=default_label(i=3), )
                        ),
                        View(layout="row", style={'background-color': 'white', 'border': '5px solid #448aff'})(View(layout='column',style={'width': 450})(
                            plotting.Figure(lambda ax: self.__pie_plot(ax) if self.__enableOnChangeCalback else None ),),
                        View(layout='column')(
                            plotting.Figure(lambda ax: self.__plot(ax) if self.__enableOnChangeCalback else None )),
                        ),



                  #      View(layout="row", )(
                #            CheckBox(text='Учет доли СП', checked=self.__model.joint_venture,
                  #                   on_change=self.__on_checkbox_changed,
                  #                   style={"width": 200 / 1.5, "align": "left", "height": 30,'background-color': '#31363b', 'color': 'white'  }),
                     #     #  plotting.Figure(lambda ax: self.plot(ax)),  # ),
                   #     ),

                        View(layout="row", style={'height': 30})(
                       #     Form(self.state, ),
                            Button("Выгрузить сводную таблицу в Excel",
                                   style={"width": 200 * 2, 'background-color': '#0091ff', 'color': 'white', "height": 20},
                                   on_click=self.__onSaveWholeTableButtonClick),
                            CheckBox(text='Учет доли СП', checked=self.__model.joint_venture,
                                     on_change=self.__on_checkbox_changed,
                                     style={"width": 200 / 1.5, "align": "center", "height": 20,
                                            'background-color': '#002033', 'color': 'white'}),

                            Button("Выгрузить объекты в Excel", style={"width": 200 * 2, 'background-color': '#0091ff','color': 'white',"height": 20 },
                                   on_click=self.__onSaveButtonClick),),

                     #   View(layout="row")(
                         #   Form(self.state, ),
                       #     Button("Выгрузить сводную таблицу в Excel", style={"width": 200 * 2, 'background-color': '#448aff', 'color': 'white' },
                       #            on_click=self.__onSaveWholeTableButtonClick), )
                ),
            )
        )


class MonitoringApp(Component):
    def __init__(self,
                 data_model: DataModelMonitoring,
                 result_path=None
                 ):
        super().__init__()
        self.__enableOnChangeCalback = True
        self.__model = data_model
        self.state = StateManager({
            "File": pathlib.Path(""),
        })
        self.result_path = result_path + '\Results.xlsx'

    def __set_field_list(self, value):
        self.__model.set_do(value)
        self.set_state()

    def __set_field(self, value):
        self.__model.set_field(value)
        self.set_state()

    def __onBlackListButtonClick(self, value):
        self.__model.black_list()
        self.set_state()

    def __onExcelCheckBox(self, value):
        self.__model.excel_export_option()
    #    self.set_state()

    def __onCompanyFormExport(self, value):
        self.__model.company_form()
        self.set_state()

    def __onImportButtonClick(self, value):
        if self.state['File'] is None:
            print('Не выбран файл!')
        else:
            self.__model.import_company_form(file_path=self.state['File'])

    def __onMappingMorButtonClick(self, value):
        self.__model.map_status_from_mor_db()
        self.set_state()

    def __onDataUploadButtonClick(self, value):
        self.__model.upload_data_for_dashboard()
        self.set_state()
    def render(self):
        return  Window(title='Программа мониторинга', )(
                View(layout="column", style={'background-color': '#31363b', "margin": 10,
                                             "font-weight": 1, "font-size": 10},)
                (View(layout="row", style={ "margin": 10,"height": 50,})(
                    Label(text='Выбор ДО', style={'align': 'center', "font-size": 20, 'color': 'white' }),
                    Label(text='Выбор месторождения', style={'align': 'center', "font-size": 20, 'color': 'white',  })
                                     ),
                 View(layout="row", style={ "margin": 10,})(
                    Dropdown(selection='ДО',
                             options=self.__model.do_list,
                             on_select=self.__set_field_list,
                             style={"margin": 40, "font-size": 20, 'height': 40 , 'background-color': '#232629', 'color': 'white'}
                             ),
                    Dropdown(selection='Месторождение',
                             options=self.__model.field_list_for_view,
                             on_select=self.__set_field,
                             style={"margin": 40, "font-size": 20, 'height': 40, 'background-color': '#232629', 'color': 'white'}
                             ),
                                            ),
                    View(layout="row", style={ "margin": 40, 'align': 'center'})(Label('Обновление базы мониторинга', style={"font-size": 20,'color': 'white', 'height': 80, 'width': 350, 'align': 'center'})),

                    View(layout="row", style={ "margin": 40,})(
                        Button("Обновление базы мониторинга",
                               #style={"margin": 10, },
                               on_click=self.__onBlackListButtonClick, style={ "font-size": 20,'background-color': '#448aff', 'color': 'white', 'height': 80}),

                    #    CheckBox(text='Выгрузка данных в Excel',
                    #             on_change=self.__onExcelCheckBox,
                    #             style={"margin": 10, }
                    #             ),
                    ),

                    View(layout="row", style={"margin": 40, })(
                        Button("Выгрузить форму для ДО",
                               # style={"margin": 10, },
                               on_click=self.__onCompanyFormExport, style={ "font-size": 20,'background-color': '#448aff', 'color': 'white', 'height': 80}),

                    ),
                    View(layout="row", style={"margin": 40, "align": 'center' })(Label('Меню загрузки форм отчета ДО', style={ "font-size": 20, 'color': 'white', 'width': 350, 'align': 'center'})),

                    View(layout="column")(
                        Form(self.state, ),
                        Button("Загрузить заполненную форму от ДО в базу",
                               on_click=self.__onImportButtonClick, style={ "margin": 40, "font-size": 20,'background-color': '#448aff', 'color': 'white', 'height': 80}), ),

                    View(layout="row", style={"margin": 40, })(

                        Button("Мэппинг объектов с базой МЭР",
                               on_click=self.__onMappingMorButtonClick, style={ "font-size": 20, 'background-color': '#448aff', 'color': 'white', 'height': 80}),
                        Button("Выгрузка данных для дашборда",
                               on_click=self.__onDataUploadButtonClick,
                               style={"font-size": 20, 'background-color': '#448aff', 'color': 'white', 'height': 80})
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