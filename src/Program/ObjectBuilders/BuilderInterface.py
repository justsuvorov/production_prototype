import abc
from Program.ObjectBuilders.FormatReader import FormatReader
from Program.BaseObject.Object import Object
from Program.BaseObject.ObjectInfo import ObjectInfo
from Program.BaseObject.Indicators import Indicators
from Program.BaseObject.Sensor import Sensor
from abc import ABC
from Program.DomainModel.ObjectList import ObjectRecord


class ObjectBuilder(ABC):
    """
      Абстрактный класс паттерна строитель для обеъкта доменной модели

      Inputs:

      format_reader: составная часть парсера данных. Сопоставляет данные с классами доменной модели
        Returns:
    build_object : Объекто доменной модели
    sensor: объект-лог ошибки

    """
    def __init__(self,
                 format_reader: FormatReader
                 ):
        self.format_reader = format_reader
        self.error = False

    @abc.abstractmethod
    def build_object(self) -> Object:
       pass

    @abc.abstractmethod
    def sensor(self) -> Sensor:
        pass

    @abc.abstractmethod
    def _create_record(self) -> ObjectRecord:
        pass


class BaseObjectBuilder(ObjectBuilder):
    """
      Абстрактный класс паттерна строитель для базового обеъкта добычи нефти доменной модели

      Inputs:

      format_reader: составная часть парсера данных. Сопоставляет данные с классами доменной модели

      """
    def __init__(self,
                 format_reader: FormatReader
                 ):
        self.format_reader = format_reader
        super().__init__(format_reader=format_reader)

    def build_object(self) -> Object:
       pass

    def sensor(self) -> Sensor:
        pass

    def _object_info(self) -> ObjectInfo:
        pass

    def _indicators(self) -> Indicators:
        pass

    def _create_record(self) -> ObjectRecord:
        pass
