from abc import ABC, abstractmethod

from BaseObject.Sensor import Sensor
from BaseObject.ObjectInfo import ObjectInfo
from BaseObject.Indicators import Indicators
from BaseObject.ObjectStatus import ObjectStatus
from BaseObject.Constraint import Constraint
import pandas as pd



class BaseObject(ABC):
    def __init__(self,
                 name: str,
                 object_info: ObjectInfo,
                 indicators: Indicators,
                 object_status: ObjectStatus,
                 sensor: Sensor,
                 constraint: Constraint = None
                 ) -> None:
        self.name = name
        self.objectInfo = object_info
        self.indicators = indicators
        self.objectStatus = object_status
        self.sensor = sensor
        self.constraint = constraint

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





