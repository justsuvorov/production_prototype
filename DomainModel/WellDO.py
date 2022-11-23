from BaseObject.BaseObject import BaseObject
from BaseObject.Sensor import Sensor
from BaseObject.ObjectInfo import ObjectInfo
from BaseObject.Indicators import Indicators
from BaseObject.ObjectStatus import ObjectStatus
from Well.WellInfo import WellInfo
import pandas as pd

class WellDO(BaseObject):
    def __init__(self,
                 name: str,
                 object_info: ObjectInfo,
                 indicators: Indicators,
                 object_status: ObjectStatus,
                 sensor: Sensor,
                 well_info: WellInfo = None
                 ) -> None:
            super().__init__(
                 name=name,
                 object_info=object_info,
                 indicators=indicators,
                 object_status=object_status,
                 sensor=sensor,
            )
            self.wellInfo = well_info

    def build(self):
        pass
    def data(self):
        pass