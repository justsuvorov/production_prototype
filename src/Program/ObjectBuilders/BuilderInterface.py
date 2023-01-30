import abc
from Program.ObjectBuilders.FormatReader import FormatReader
from Program.BaseObject.Object import Object
from Program.BaseObject.ObjectInfo import ObjectInfo
from Program.BaseObject.Indicators import Indicators
from Program.BaseObject.Sensor import Sensor
from abc import ABC
from Program.DomainModel.ObjectList import ObjectRecord


class ObjectBuilder(ABC):
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
