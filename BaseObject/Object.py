from abc import ABC, abstractmethod

from BaseObject.Sensor import Sensor
from BaseObject.ObjectInfo import ObjectInfo
from BaseObject.Indicators import Indicators
from BaseObject.ObjectStatus import ObjectStatus
from BaseObject.Constraint import Constraint


class Object(ABC):

    def __init__(self,
                 name: str,
                 indicators: Indicators,
                 sensor: Sensor):
        self.name = name
        self.indicators = indicators
        self.sensor = sensor

    @abstractmethod
    def build(self):
        pass
