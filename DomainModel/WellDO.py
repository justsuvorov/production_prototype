from BaseObject.BaseObject import BaseObject
from BaseObject.Sensor import Sensor
from BaseObject.ObjectInfo import ObjectInfo
from BaseObject.Indicators import Indicators
from Well.WellInfo import WellInfo
from DomainModel import DomainModel


class WellDO(BaseObject):
    def __init__(self,
                 name: str,
                 object_info: ObjectInfo,
                 indicators: Indicators,
                 sensor: Sensor,
                 link: list = None,
                 well_info: WellInfo = None
                 ) -> None:
            super().__init__(
                 name=name,
                 object_info=object_info,
                 indicators=indicators,
                 sensor=sensor,
                 link=link
            )
            self.wellInfo = well_info

    def build(self):
        pass
    def data(self):
        pass

    @classmethod
    def from_data(cls, domain_model: DomainModel, name: str):
        try:
            return domain_model.wellDO(name)
        except:
            print('No data for this well')