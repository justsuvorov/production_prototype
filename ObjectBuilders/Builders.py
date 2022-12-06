import pandas as pd

from ObjectBuilders.BuilderInterface import *
from ObjectBuilders.FormatReader import FormatReader
from BaseObject.Object import Object
from BaseObject.ObjectInfo import ObjectInfo
from BaseObject.Indicators import Indicators
from BaseObject.Sensor import Sensor
from DomainModel.ObjectList import ObjectRecord
from BaseObject.Parser import Parser

class WellBuilder(BaseObjectBuilder):

    def __init__(self,
                 format_reader: FormatReader,
                 data: pd.DataFrame):
        self.format_reader = format_reader
        super().__init__(format_reader=format_reader)
        self.data = data

    def build_object(self) -> Object:
       pass

    def sensor(self) -> Sensor:
        pass

    def _object_info(self) -> ObjectInfo:
        return self.format_reader(self.data)

    def _indicators(self) -> Indicators:
        pass

    def _create_record(self) -> ObjectRecord:
        pass

    def _wellinfo(self):
        pass

class PadBuilder(BaseObjectBuilder):

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

    def _padinfo(self):
        pass

class ClusterBuilder(BaseObjectBuilder):

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

    def _padinfo(self):
        pass

class DomainModelBuilder(ObjectBuilder):
    def __init__(self,
                 parser: Parser,
                 format_reader: FormatReader,
                 ):
        self.paser = parser
        self.format_reader = format_reader
        super().__init__(format_reader=format_reader)

    def build_object(self) -> Object:
        domain_model = []
        data = self._data()
        for row in data.iterrows():

            domain_model.append( WellBuilder(format_reader=self.format_reader, data=row)._object_info())
        return domain_model

    def sensor(self) -> Sensor:
        pass

    def _create_record(self) -> ObjectRecord:
        pass

    def _data(self):
        return self.paser.data()

