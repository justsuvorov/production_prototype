import os
from typing import Callable

import edifice
from edifice import Label,  Slider, Dropdown, View, CheckBox,TextInput,  Component, StateManager, Window, Button, ScrollView, RadioButton
from edifice.components.forms import FormDialog, Form
from edifice.components import plotting
from Program.GUI.data_model import DataModel, ModelProxy
from Program.GUI.data_model_monitoring import *
from Program.GUI.data_value import DataValue
from Program.GUI.components import default_label, DefaultSlider, add_divider, DefaultDropdown
import pathlib
from copy import deepcopy




class OperBalancerApplication(Component):
    def __init__(self,
                 model_proxy: DataModel,
           #      data_modelFull: DataModel,
           #      data_modelVbd: DataModel,
                 result_path = None,
            #     vbd_data_model: DataModel = None,
                 ):
        super().__init__()
        self.__result_path = result_path
        self._model_index = False
  #      self._modelFull = data_modelFull
  #      self._modelVbd = data_modelVbd
        self._model = model_proxy
        self._enableOnChangeCalback = True
        self._refresh_plots = True
        self.state = StateManager({
            "File": pathlib.Path(""),
        })
        self.result_path = result_path +'\Results.xlsx'
        self.names = []
        self.gpn_value = self._model.company_value.toFloat


    def _on_dropdown_select(self, value):
        self._model.choose_month(value)
        self.gpn_value = self._model.company_value.toFloat
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_gpn_changed(self, value):
        self._model.on_gpn_change(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_vostok_changed(self, value):

        self._model.set_vostok_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_megion_changed(self, value):

        self._model.set_megion_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_messoyaha_changed(self, value):
        self._model.set_messoyaha_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_nng_changed(self, value):
        self._model.set_nng_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_orenburg_changed(self, value):
        self._model.set_orenburg_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_hantos_changed(self, value):
        self._model.set_hantos_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_yamal_changed(self, value):
        self._model.set_yamal_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_polar_changed(self, value):
        self._model.set_polar_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_shelf_changed(self, value):
        self._model.set_shelf_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_meretoyaha_changed(self, value):
        self._model.set_meretoyaha_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_spd_changed(self, value):
        self._model.set_spd_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_palyan_changed(self, value):
        self._model.set_palyan_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_angara_changed(self, value):
        self._model.set_angara_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_arctic_changed(self, value):
        self._model.set_arctic_value(value)
        self._enableOnChangeCalback = False
        self.set_state()
        self._enableOnChangeCalback = True

    def _on_checkbox_changed(self,value ):
        self._enableOnChangeCalback = False
        self._model.choose_scenario()
        self.set_state()
        self._enableOnChangeCalback = True

    def _onSaveButtonClick(self, value):
        if self.state['File'] ==pathlib.Path(""):
            path = pathlib.Path(self.result_path)
        else:
            path = self.state['File']
        self._model.save_results(path=path)
        os.startfile(path)
        self._enableOnChangeCalback = False
       # self.set_state()
        self._enableOnChangeCalback = True

    def _onSaveWholeTableButtonClick(self, value):
        if self.state['File'] == pathlib.Path(""):
            path = pathlib.Path(self.result_path)
        else:
            path = self.state['File']
        self._model.save_overal_results(path=path)
        os.startfile(path)
        self._enableOnChangeCalback = False
        # self.set_state()
        self._enableOnChangeCalback = True

    def _on_Reset_click_button(self, value):
        self._on_gpn_changed(value=self._model.company_value.toFloat)
        self._enableOnChangeCalback = False

        self.set_state()
        self._enableOnChangeCalback = True

    def _plot_draw(self, ax):

        x, y, x2, y2 = self._model.plot_coordinates()
        colors = [
            # matplotlib named colors
            'cornflowerblue', 'tomato', 'grey', 'gold',
            "orchid", 'green', 'blue']
        i = 0
        xlim = 6000
        ylim = 10


        for key in x:
            line = ax.plot(x[key], y[key], 5, color=colors[i], linewidth=2)
            line[-1].set_label(key)
            i += 1

        ax.legend(markerscale=1.1)

        for key in x:
            ax.plot(x2[key], y2[key], color='#31363b', marker="o", markersize=8, label=None)
        ax.grid(True)
        ax.set(xlabel='Среднесуточная добыча, т/сут.', ylabel='FCF/Q, тыс.руб/т.',
               xlim=(0, xlim),
               ylim=(0, ylim,),
               title='Удельный FCF на тонну',
               )

    def _plot(self, ax):
        self._refresh_plots= not self._refresh_plots
        if self._refresh_plots:
            self._on_angara_changed(0)
        self._plot_draw(ax)

    def _pie_plot(self, ax,):

        x2, values = self._model.pie_plot_coordinates()
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

        ax.pie(x2, labels=labels_for_view, wedgeprops=dict(width=0.5), textprops={'fontsize': 8},
               colors=[
                   # matplotlib named colors
                    'cornflowerblue', 'tomato', 'gold', 'orchid', 'green',
                   "#77BFE2", 'blue']
               )


    def _onModelChangeClick(self, value):
        self._enableOnChangeCalback = False
        self._model_index = not self._model_index
        self._model.change_model()
        self._model.choose_month(value=self._model.months[self._model.index])
        self.gpn_value = self._model.company_value.toFloat
        self.set_state()
        self._enableOnChangeCalback = True

    def __onSliderComplete(self, value):

        self._on_gpn_changed(value=self.gpn_value)
   #     self.set_state()

    def __onInputComplete(self, value):
        self._on_gpn_changed(value)

    def set_value_gpn(self, value):
        self.gpn_value = value
    #    self.set_state()


    def render(self):

        if self._model_index:
            label = 'Прирост '
            label2 = 'Прирост '
        else:
            label = 'Сокращение '
            label2 = 'Потери '
        return Window(title='Оперативная балансировка добычи', )(
            View(layout="column", style={'background-color': '#002033',
                                         "margin": 10,
                                         "font-weight": 2,
                                         "font-size": 15}, )  # """ style={"margin": 10, "font-weight": 1},"""
                (
                DefaultDropdown(value=self._model.target,
                                options=self._model.months,
                                onSelect=self._on_dropdown_select if self._enableOnChangeCalback else None),

                ScrollView(layout="column", style={'height': 200})
                    (View(layout="row", style={'background-color': '#002033', 'color': 'white'})(
                    add_divider(Label('ДО', style=default_label(i=2)),
                                Label('Прогноз добычи, т/сут.', style=default_label(i=2)),
                                Label('Откл. по добыче, т/сут.', style=default_label(i=2)),
                                Label('Итоговая добыча, т/сут.', style=default_label(i=2)), ),
                ),

                    *[add_divider(Label(name, style={'background-color': '#002033', 'color': 'white', "font-size": 13}),
                                  Label(constraint, style=default_label(i=2)),
                                  Label(value, style=default_label(i=2)),
                                  Label(result.round(), style=default_label(i=2)),
                                  ) for name, constraint, value, result in zip(self._model.full_company_list,
                                                                               self._model.forecast_list,
                                                                               self._model.crude_list,
                                                                               self._model.result_crude_list)],

                ),

                View(layout='column', style={"margin": 1, "font-weight": 1})(
                    View(layout="row", style={'height': 30})(Label('Итог', style=default_label(i=2)),
                                                             Label(self._model.forecast_sum.toStr,
                                                                   style=default_label(i=5)),
                                                             Label(self._model.crude_sum.toStr,
                                                                   style=default_label(i=5)),
                                                             Label(self._model.result_crude_sum.toStr,
                                                                   style=default_label(i=5)),
                                                             ),

                    View(layout="row", style={'height': 30})(Label('Квота МЭ', style=default_label(i=2)),
                                                             Label(self._model.quota.toStr,
                                                                   style=default_label(i=5)),
                                                             Label('', style=default_label(i=2)),
                                                             Label('', style=default_label(i=2)),

                                                             ),
                    View(layout="row", style={'align': 'left', 'height': 30})(RadioButton(text='Наращивание добычи',
                                                                                          checked=self._model_index,
                                                                                          on_change=self._onModelChangeClick,
                                                                                          style={'width': 500,
                                                                                                 'background-color': '#002033',
                                                                                                  'color': 'white', "font-size": 13}),

                                                                ),

                    View(layout="row", style={'height': 40})(
                        Label('ДО', style=default_label(i=1), ),
                        Label(label + 'добычи',
                              style={"width": 1.5 * 200, 'background-color': '#002033', 'color': 'white',
                                     "font-size": 13}, ),
                        Button('Сбросить настройки', on_click=self._on_Reset_click_button,
                               style={'background-color': '#0091ff', 'color': 'white', 'height': 20, "font-size": 13}),

                        Label('т/сут.', style=default_label(i=3)),
                        Label(label2 + 'FCF, млн.руб.', style=default_label(i=3)),

                    ),

                    View(layout="row", style={'background-color': '#002033', 'color': 'white', 'height': 30})(
                        Label('ГПН', style=default_label(i=1), ),
                        Slider(value=self.gpn_value,
                               min_value=self._model.min_value['ГПН'].toFloat,
                               max_value=self._model.max_value['ГПН'].toFloat,
                               on_change = self.set_value_gpn,
                               on_mouse_up=self.__onSliderComplete,
                               ),

                        TextInput(text=self._model.company_value.toStr,
                     #             on_change=self._on_gpn_changed if self._enableOnChangeCalback else None,
                                  on_edit_finish=self.__onInputComplete,
                                  style=default_label(i=6)),
                        Label(self._model.fcf_sum.toStr,
                              style=default_label(i=3))
                    ),



                    #        Label("", style={"width": 200, "align": 'center'}, ),

                    ScrollView(layout="column", style={'background-color': '#002033', 'color': 'white', 'height': 200})(

                        DefaultSlider(value=self._model.vostok_value,
                                      fcf_value=self._model.vostok_fcf,
                                      label=self._model.company_names[0],
                                      min_value=self._model.min_value['Восток'],
                                      max_value=self._model.max_value['Восток'],
                                      onChanged=self._on_vostok_changed if self._enableOnChangeCalback else None,

                                      ),


                        DefaultSlider(value=self._model.megion_value,
                                      fcf_value=self._model.megion_fcf,
                                      label=self._model.company_names[1],
                                      min_value=self._model.min_value['Мегионнефтегаз'],
                                      max_value=self._model.max_value['Мегионнефтегаз'],
                                      onChanged=self._on_megion_changed if self._enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self._model.messoyaha_value,
                                      fcf_value=self._model.messoyaha_fcf,
                                      label=self._model.company_names[2],
                                      min_value=self._model.min_value['Мессояханефтегаз'],
                                      max_value=self._model.max_value['Мессояханефтегаз'],
                                      onChanged=self._on_messoyaha_changed if self._enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self._model.nng_value,
                                      fcf_value=self._model.nng_fcf,
                                      label=self._model.company_names[3],
                                      min_value=self._model.min_value['ННГ'],
                                      max_value=self._model.max_value['ННГ'],
                                      onChanged=self._on_nng_changed if self._enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self._model.orenburg_value,
                                      fcf_value=self._model.orenburg_fcf,
                                      label=self._model.company_names[4],
                                      min_value=self._model.min_value['Оренбург'],
                                      max_value=self._model.max_value['Оренбург'],
                                      onChanged=self._on_orenburg_changed if self._enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self._model.hantos_value,
                                      fcf_value=self._model.hantos_fcf,
                                      label=self._model.company_names[5],
                                      min_value=self._model.min_value['Хантос'],
                                      max_value=self._model.max_value['Хантос'],
                                      onChanged=self._on_hantos_changed if self._enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self._model.yamal_value,
                                      fcf_value=self._model.yamal_fcf,
                                      label=self._model.company_names[6],
                                      min_value=self._model.min_value['Ямал'],
                                      max_value=self._model.max_value['Ямал'],
                                      onChanged=self._on_yamal_changed if self._enableOnChangeCalback else None,

                                      ),

                        DefaultSlider(value=self._model.polar_value,
                                      fcf_value=self._model.polar_fcf,
                                      label='Заполярье',
                                      min_value=self._model.min_value['Заполярье'],
                                      max_value=self._model.max_value['Заполярье'],
                                      onChanged=self._on_polar_changed if self._enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self._model.shelf_value,
                                      fcf_value=self._model.shelf_fcf,
                                      label='Шельф',
                                      min_value=self._model.min_value['Шельф'],
                                      max_value=self._model.max_value['Шельф'],
                                      onChanged=self._on_shelf_changed if self._enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self._model.meretoyaha_value,
                                      fcf_value=self._model.meretoyaha_fcf,
                                      label='Меретояханефтегаз',
                                      min_value=self._model.min_value['Меретояханефтегаз'],
                                      max_value=self._model.max_value['Меретояханефтегаз'],
                                      onChanged=self._on_meretoyaha_changed if self._enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self._model.palyan_value,
                                      fcf_value=self._model.palyan_fcf,
                                      label='Пальян',
                                      min_value=self._model.min_value['Пальян'],
                                      max_value=self._model.max_value['Пальян'],
                                      onChanged=self._on_palyan_changed if self._enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self._model.spd_value,
                                      fcf_value=self._model.spd_fcf,
                                      label='СПД',
                                      min_value=self._model.min_value['СПД'],
                                      max_value=self._model.max_value['СПД'],
                                      onChanged=self._on_spd_changed if self._enableOnChangeCalback else None,
                                      ),

                        DefaultSlider(value=self._model.arctic_value,
                                      fcf_value=self._model.arctic_fcf,
                                      label='Арктикгаз',
                                      min_value=self._model.min_value['Арктикгаз'],
                                      max_value=self._model.max_value['Арктикгаз'],
                                      onChanged=self._on_arctic_changed if self._enableOnChangeCalback else None,
                                      ),
                        DefaultSlider(value=self._model.angara_value,
                                      fcf_value=self._model.angara_fcf,
                                      label='Ангара',
                                      min_value=self._model.min_value['Ангара'],
                                      max_value=self._model.max_value['Ангара'],
                                      onChanged=self._on_angara_changed if self._enableOnChangeCalback else None,
                                      ),
                    ),

                    View(layout="row", style={'height': 30})(
                        Label('', ),
                        Label('Сумма',
                              style={"width": 450, "align": "right", 'background-color': '#002033', 'color': 'white',
                                     "font-size": 13, 'height': 30}, ),
                        Label(round(self._model.crude_sum.toFloat), style=default_label(i=3)),
                        Label(self._model.fcf_sum.toStr, style=default_label(i=3), )
                    ),
                    View(layout="row", style={'background-color': 'white', 'border': '5px solid #448aff', })(
                        View(layout='column', style={'width': 650, })(
                            plotting.Figure(
                                lambda ax: self._pie_plot(ax) if self._enableOnChangeCalback else None), ),
                        View(layout='column')(
                            plotting.Figure(lambda ax: self._plot(ax) if self._enableOnChangeCalback else None)),
                    ),

                    View(layout="row", style={'height': 30})(
                        #     Form(self.state, ),
                        Button("Выгрузить сводную таблицу в Excel",
                               style={"width": 200 * 2, 'background-color': '#0091ff', 'color': 'white', "height": 20,
                                      "font-size": 13},
                               on_click=self._onSaveWholeTableButtonClick),
                        CheckBox(text='Учет доли СП', checked=self._model.joint_venture,
                                 on_change=self._on_checkbox_changed,
                                 style={"width": 200 / 1.5, "align": "center", "height": 20,
                                        'background-color': '#002033', 'color': 'white', "font-size": 13}),

                        Button("Выгрузить объекты в Excel",
                               style={"width": 200 * 2, 'background-color': '#0091ff', 'color': 'white', "height": 20,
                                      "font-size": 13},
                               on_click=self._onSaveButtonClick), ),

                    #   View(layout="row")(
                    #   Form(self.state, ),
                    #     Button("Выгрузить сводную таблицу в Excel", style={"width": 200 * 2, 'background-color': '#448aff', 'color': 'white' },
                    #            on_click=self._onSaveWholeTableButtonClick), )
                ),
            )
        )