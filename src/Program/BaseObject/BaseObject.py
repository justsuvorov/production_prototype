from abc import ABC, abstractmethod

from Program.BaseObject.Sensor import Sensor
from Program.BaseObject.ObjectInfo import ObjectInfo
from Program.BaseObject.Indicators import Indicators
from Program.BaseObject.ObjectStatus import ObjectStatus
from Program.BaseObject.Constraint import Constraint
import pandas as pd
from Program.BaseObject.Object import Object



class BaseObject(Object):
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

    def change_activity(self):
        self.object_info.object_activity = not self.object_info.object_activity






