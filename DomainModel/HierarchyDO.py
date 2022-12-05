from BaseObject.BaseObject import Object
from BaseObject.Sensor import Sensor
from BaseObject.ObjectInfo import ObjectInfo
from BaseObject.Indicators import Indicators
from datetime import date
from BaseObject.ObjectStatus import ObjectStatus
from Well.WellInfo import WellInfo
import pandas as pd
from DomainModel import DomainModel

class HierarchyDO(Object):
    def __init__(self,
                 name: str,
                 indicators: Indicators,
                 sensor: Sensor,
                 last_fact_date : date
                 ):
        self.name = name
        self.indicators = indicators
        self.sensor = sensor
        self.last_fact_date = last_fact_date
        super().init(name=name,
                     indicators=indicators,
                     sensor=sensor)
    def build(self):
        pass