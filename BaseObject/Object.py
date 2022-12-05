from abc import ABC, abstractmethod

from BaseObject.Sensor import Sensor
from BaseObject.ObjectInfo import ObjectInfo
from BaseObject.Indicators import Indicators
from BaseObject.ObjectStatus import ObjectStatus
from BaseObject.Constraint import Constraint


class Object(ABC):

    def __init__(self,
                 name: str,
                 sensor: Sensor,
                 link: list = None):
        self.name = name
        self.sensor = sensor
        self.link = link

    @abstractmethod
    def build(self):
        pass