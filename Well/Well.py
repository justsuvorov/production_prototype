from Well.Sensor import Sensor

from Well.Indicator import ArrayIndicator, ValueIndicator
from Well.Indicators import Indicators
from Well.WellStatus import WellStatus
from Well.PlastInfo import PlastInfo
from Well.WellInfo import WellInfo, ObjectInfo

import datetime as dt
from typing import Dict, List, Optional, Tuple

class Well:
    def __init__(self,
                 id: int,
                 objectInfo: ObjectInfo,
                 indicators: Indicators,
                 wellStatus: WellStatus,
                 sensor: Sensor,
                ) -> None:
        self.id = id
        self.wellInfo = objectInfo
        self.indicators = indicators
        self.wellStatus = wellStatus
        self.sensor = sensor

    @classmethod
    def default(cls, id):
        objectInfo = ObjectInfo()
     #       wellType='oil',
    #        plastInfo=PlastInfo()
    #    )
        sensor = Sensor()
        indicators = Indicators()
        wellstatus = WellStatus()

        return cls(
            id,
            objectInfo,
            indicators,
            wellstatus,
            sensor,
        )

    def build(self):
        pass

    def data(self):
        pass