from Program.BaseObject.BaseObject import BaseObject
from Program.BaseObject.Sensor import Sensor
from Program.BaseObject.ObjectInfo import ObjectInfo
from Program.BaseObject.Indicators import Indicators
from Program.Well.WellInfo import WellInfo
from Program.DomainModel import DomainModel


class PadDO(BaseObject):
    """
    Класс куста

    Inputs:
    name: имя объекта (название)
    object_info: класс-контейнер основной информации об объекте. Тип, список связей, статус
    indicators: показатели объекта с описанием сценария. Показатели - словари
    sensor: класс-логгер ошибок внутри объекта
    link: словарь ссылок на объекты иерархии
    pad_info: класс дополнительной информации о кусте

    """
    def __init__(self,
                 name: str,
                 object_info: ObjectInfo,
                 indicators: Indicators,
                 sensor: Sensor,
                 link: dict = None,
                 pad_info: WellInfo = None
                 ) -> None:
            super().__init__(
                 name=name,
                 object_info=object_info,
                 indicators=indicators,
                 sensor=sensor,
                 link=link,
            )
            self.pad_info = pad_info


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
