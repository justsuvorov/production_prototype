import edifice
import numpy as np
import pandas as pd
from copy import deepcopy, copy
from typing import Callable, Mapping, Text, Any
from Program.GUI.data_value import DataValue

from Program.Production.GfemScenarios import *
from edifice._component import PropsDict
from edifice import Label, Slider, Dropdown, View, CheckBox, TextInput, Component, StateManager, Window, Button, \
    ScrollView, QtWidgetComponent, WidgetComponent, BaseComponent
from edifice.components.forms import FormDialog, Form
from edifice.components import plotting
from edifice import Timer



def add_divider(comp, comp2, comp3, comp4):
    return View(layout="row", style={'background-color': 'white'}) \
            (View(layout="column", style={'background-color': 'white'})(
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


def default_label(i):
    label_width = 200
    """
    if i == 1:  #
        return {"width": label_width}
    if i == 2:  # верхняя таблица
        return {"align": "center", 'height': 30}
    if i == 3:
        return {"width": label_width / 2, "margin": 5, "align": "center"}
    if i == 4:
        return {"width": 200, "margin": 5, "align": "right"}
    if i == 5:
        return {"align": "center", 'height': 30, 'font-weight': 10}
    if i == 6:
        return {"width": label_width / 2, "margin": 5, "align": "center", "border": "0px"}
        'background-color': '#31363b',
        'background-color': '#232629',
"""

    if i == 1:  #
        return {"width": label_width, 'background-color': '#002033', 'color': 'white', "font-size": 13}
    if i == 2:  # верхняя таблица
        return {"align": "center", 'height': 30, 'background-color': '#002033', 'color': 'white', "font-size": 13}
    if i == 3:
        return {"width": label_width / 2, "margin": 5, "align": "center", 'background-color': '#002033', 'color': 'white', "font-size": 13}
    if i == 4:
        return {"width": 200, "margin": 5, "align": "right", 'background-color': '#002033', 'color': 'white', "font-size": 13}
    if i == 5:
        return {"align": "center", 'height': 30, 'font-weight': 10, 'background-color': '#002033', 'color': 'white', "font-size": 13}
    if i == 6:
        return {"width": label_width / 2, "margin": 5, "align": "center", "border": "0px", 'background-color': '#002033', 'color': 'white', "font-size": 13}



class DefaultDropdown(Component):
    def __init__(self,
                 options,
                 onSelect: Callable[[str or float], None],
                 value: DataValue
                 ):
        self.__label_value = value
        self.__options = options
        super().__init__()
        self.__onSelect = onSelect
        self.__value = DataValue('0')

    def __onSelectChanged(self, value):
        #  print(f'new value: {value}')
        self.__value.update(value)
        if self.__onSelect:
            self.__onSelect(value)

    def render(self):
        return View(layout="row", style={"margin": 10, "font-weight": 1})(
            Label('Месяц прогноза', style=default_label(i=1), ),
            Dropdown(selection='Месяц',
                     options=self.__options,
                     on_select=self.__onSelect,
                     style={'background-color': '#232629', 'color': 'white', "font-size": 13}
                     ),
            Label('', style={"width": 30}, ),
            Label('Необходимо срезать/нарастить добычи,  т/сут.', style=default_label(i=1), ),
            Label(self.__label_value.toStr, style=default_label(i=1), )
        )

 #   def should_update(self, newprops: PropsDict, newstate: Mapping[Text, Any]) -> bool:
 #       return True


class DefaultSlider(Component):
    def __init__(self,
                 label: str,
                 value: DataValue,
                 fcf_value: DataValue,

                 min_value: DataValue,
                 max_value: DataValue,
                 onChanged: Callable[[str or float], None] = None,
                 ):
        super().__init__()

        self.__label = label
        self.__value = value
        self.__fcf_value = fcf_value
        self.__min_value = min_value
        self.__max_value = max_value
        self.__onChanged = onChanged


    def render(self):

        return View(layout="row", style={'background-color': '#002033', 'color': 'white', 'height': 30 })(
            Label(self.__label, style=default_label(i=1), ),
            Slider(value=self.__value.toFloat,
                   min_value=self.__min_value.toFloat,
                   max_value=self.__max_value.toFloat,
                   #    on_mouse_up=lambda value1: self.control(copmany=name, value=value),
                   #     on_mouse_down=lambda value1: self.control(copmany=name, value=value),
                   # on_change=self.__onValueChanged,
                   on_change=self.__onValueChanged,
                   on_mouse_up=self.__onSliderComplete,
                  ),

            TextInput(text=self.__value.toStr,
                      #        on_click=lambda value1 :self.control(copmany=name, value=value),
                      on_change=self.__onValueChanged,
                      on_edit_finish=self.__onInputComplete,
                      style=default_label(i=6)),
            #  TextInput(round(float(value), 1), on_change=lambda value: self.set_do_value(value=float(value), copmany=name)),
            Label(self.__fcf_value.toStr,
                  style=default_label(i=3))
        )

    def __onSliderComplete(self, value):
        if self.__onChanged:
          self.__onChanged(self.__value.toFloat)



    def __onInputComplete(self):
        if self.__onChanged:
            self.__onChanged(self.__value.toFloat)


    def __onValueChanged(self, value):
   #     print(f'new value: {value}')
        self.__value.update(value)

    def should_update(self, newprops: PropsDict, newstate: Mapping[Text, Any]) -> bool:
        return True

