from abc import ABC, abstractmethod

from Program.BaseObject.Sensor import Sensor
from Program.BaseObject.ObjectInfo import ObjectInfo
from Program.BaseObject.Indicators import Indicators
from Program.BaseObject.ObjectStatus import ObjectStatus
from Program.BaseObject.Constraint import Constraint
import pandas as pd
from Program.BaseObject.Object import Object


class BaseObject(Object):

    """
    Абстрактный класс базового объекта добычи нефти

    Inputs:
    name: имя объекта (название)
    object_info: класс-контейнер основной информации об объекте. Тип, список связей, статус
    indicators: показатели объекта с описанием сценария. Показатели - словари
    sensor: класс-логгер ошибок внутри объекта
    link: словарь ссылок на объекты иерархии


    """
    def __init__(self,
                 name: str,
                 object_info: ObjectInfo,
                 indicators: Indicators,
                 sensor: Sensor,
                 link: dict = None,
                 ) -> None:
        self.name = name
        self.object_info = object_info
        self.indicators = indicators
        self.sensor = sensor
        self.link = link

        super().__init__(name=name,
                         sensor=sensor,
                         link=link
                         )

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def data(self):
        pass

    def change_activity(self):
        self.object_info.object_activity = not self.object_info.object_activity
