import pandas as pd

from ObjectBuilders.BuilderInterface import *
from ObjectBuilders.FormatReader import FormatReader
from BaseObject.Object import Object
from BaseObject.ObjectInfo import ObjectInfo
from BaseObject.Indicators import Indicators
from BaseObject.Sensor import Sensor
from DomainModel.ObjectList import ObjectRecord
from BaseObject.Parser import Parser
from constants import MERNames, StringConstants

class WellBuilder(BaseObjectBuilder):

    def __init__(self,
                 format_reader: FormatReader,
                 data: pd.DataFrame):
        self.format_reader = format_reader
        super().__init__(format_reader=format_reader)
        self.data = data
        self.error = False
        self.wells_count = 0

    def build_object(self) -> Object:
       return WellDO(
           name=self.format_reader.names(self.data)['Well'],
           object_info=self._object_info(),
           indicators=self._indicators(),
           sensor=self.sensor(),
       )

    def sensor(self) -> Sensor:
        return Sensor()

    def _object_info(self) -> ObjectInfo:
        return self.format_reader.object_info(self.data)

    def _indicators(self) -> Indicators:
        return self.format_reader.indicators(self.data)

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
        self.parser = parser
        self.format_reader = format_reader
        super().__init__(format_reader=format_reader)
        self.object_id = 0
        self.object_list = {}

    def build_object(self) -> Object:
        domain_model = []
        data = self._data()

        domain_model.append(self._create_wells(data))
        return domain_model

    def sensor(self) -> Sensor:
        pass

    def _create_record(self) -> ObjectRecord:
        pass

    def _data(self):
        return self.parser.data()

    def _create_wells(self, data):
        wells = []
        well_names = data[MERNames.WELL].unique()
        for name in well_names:
            data_temp = data.loc[data[MERNames.WELL] == name].to_numpy()
            well = WellBuilder(
                format_reader=self.format_reader,
                data=data_temp).build_object()
            self.object_id += 1
            self.object_list[self.object_id] = ObjectRecord.create(object=well,
                                                                   type_of_object='Well')
            wells.append(well)
        return wells

