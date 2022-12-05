from abc import ABC, abstractmethod

from BaseObject.Sensor import Sensor
from BaseObject.ObjectInfo import ObjectInfo
from BaseObject.Indicators import Indicators
from BaseObject.ObjectStatus import ObjectStatus
from BaseObject.Constraint import Constraint
import pandas as pd
from BaseObject.Object import Object



class BaseObject(Object):
    def __init__(self,
                 name: str,
                 object_info: ObjectInfo,
                 indicators: Indicators,
                 sensor: Sensor,
                 link: list = None,
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

  #  @abstractmethod
  #  def init_from_config(cls, id: str,  *args):
  #      "Создание default объектов через config файл"

  #  @abstractmethod
  #  def init_from_df(cls, data: pd.DataFrame,  *args):
  #      "Создание объектов из датафрейма"

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def data(self):
        pass





