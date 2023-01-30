from Program.BaseObject.BaseObject import Object
from Program.BaseObject.Sensor import Sensor
from Program.BaseObject.Indicators import Indicators
from datetime import date


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