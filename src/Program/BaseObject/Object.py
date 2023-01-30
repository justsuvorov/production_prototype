from abc import ABC, abstractmethod

from Program.BaseObject.Sensor import Sensor
from Program.BaseObject.ObjectInfo import ObjectInfo
from Program.BaseObject.Indicators import Indicators
from Program.BaseObject.ObjectStatus import ObjectStatus
from Program.BaseObject.Constraint import Constraint


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