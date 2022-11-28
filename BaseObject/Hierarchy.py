from abc import ABC, abstractmethod

import datetime as dt
from BaseObject.Object import Object
from BaseObject.Sensor import Sensor
from BaseObject.ObjectInfo import ObjectInfo
from BaseObject.Indicators import Indicators
from BaseObject.ObjectStatus import ObjectStatus
from BaseObject.Constraint import Constraint
import pandas as pd

class Hierarchy(ABC):
    def __init__(self,
                 name: str,
                 last_fact_date: dt.date,
                 object_list: dict,
                 indicators: Indicators,
                 sensor: Sensor,

                 ):
        self.name = name
        self.last_fact_date = last_fact_date
        self.object_list = object_list
        self.indicators = indicators
        self.sensor = sensor
"""
        super().__init__(name=name,
                         indicators=indicators,
                         sensor=sensor,
                         )

"""