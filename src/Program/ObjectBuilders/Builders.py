import pandas as pd

from Program.BaseObject.Indicators import Indicators
from Program.BaseObject.Object import Object
from Program.BaseObject.ObjectInfo import ObjectInfo
from Program.BaseObject.Sensor import Sensor
from Program.DomainModel.ObjectList import ObjectRecord
from Program.ObjectBuilders.FormatReader import FormatReader
from Program.ObjectBuilders.Parser import Parser
from Program.ObjectBuilders.BuilderInterface import BaseObjectBuilder, ObjectBuilder
from Program.DomainModel.WellDO import WellDO
from Program.DomainModel.PadDO import PadDO
from Program.DomainModel.Cluster import ClusterDO


class WellBuilder(BaseObjectBuilder):

    def __init__(self,
                 format_reader: FormatReader,
                 data: pd.DataFrame):
        self.format_reader = format_reader
        super().__init__(format_reader=format_reader)
        self.data = data

    def build_object(self) -> Object:

       return WellDO(
           name=self.format_reader.names(self.data)['Well'],
           object_info=self._object_info(),
           indicators=self._indicators(),
           sensor=self.sensor(),
           link=self.format_reader.names(self.data)
       )

    def sensor(self) -> Sensor:
        return Sensor(self.error)

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
                 format_reader: FormatReader,
                 data: pd.DataFrame
                 ):
        self.format_reader = format_reader
        self.data = data
        super().__init__(format_reader=format_reader)

    def build_object(self) -> Object:
        return PadDO(
            name=self.format_reader.names(self.data)['Pad'],
            object_info=self._object_info(),
            indicators=self._indicators(),
            sensor=self.sensor(),
            link=self.format_reader.names(self.data)
        )


    def sensor(self) -> Sensor:
        return Sensor(self.error)

    def _object_info(self) -> ObjectInfo:
        return self.format_reader.object_info(self.data)

    def _indicators(self) -> Indicators:
        return Indicators(indicators={})

    def _create_record(self) -> ObjectRecord:
        pass

    def _padinfo(self):
        pass

class ClusterBuilder(BaseObjectBuilder):

    def __init__(self,
                 format_reader: FormatReader,
                 data,
                 ):
        self.format_reader = format_reader
        self.data = data
        super().__init__(format_reader=format_reader)

    def build_object(self) -> Object:
        return ClusterDO(
            name=self.format_reader.names(self.data)['Cluster'],
            object_info=self._object_info(),
            indicators=self._indicators(),
            sensor=self.sensor(),
            link=self.format_reader.names(self.data)
        )

    def sensor(self) -> Sensor:
        return Sensor(self.error)

    def _object_info(self) -> ObjectInfo:
        return self.format_reader.object_info(self.data)

    def _indicators(self) -> Indicators:
        return Indicators(indicators={})

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

    def build_object(self, only_wells: bool = None) -> Object:
        domain_model = []
        data = self._data()

        domain_model.append(self._create_wells(data))
        if only_wells is None:
            domain_model.append(self._create_pads(data))
            domain_model.append(self._create_clusters(data))
   #     self._create_links()


        return domain_model

    def sensor(self) -> Sensor:
        pass

    def _create_record(self) -> ObjectRecord:
        pass

    def _data(self):
        return self.parser.data()

    def _create_wells(self, data: pd.DataFrame):
        wells = []
        #well_names = data['Скважина'].unique()
        #well_names = data['Скважина']
        for index, well_data in data.iterrows():
            data_temp = well_data.to_numpy()
            well = WellBuilder(
                format_reader=self.format_reader,
                data=data_temp).build_object()
            wells.append(well)
            self.object_id += 1
            self.object_list[self.object_id] = ObjectRecord.create(object=well,
                                                                   type_of_object='Well')
        """ 
        for name in well_names:
            
            data_temp = data.loc[data['Скважина'] == name].to_numpy()
            shape = data_temp.shape
            if shape[0] > 1:
                for string in data_temp:
                    well = WellBuilder(
                        format_reader=self.format_reader,
                        data=string).build_object()
                    wells.append(well)
                    self.object_id += 1
                    self.object_list[self.object_id] = ObjectRecord.create(object=well,
                                                                           type_of_object='Well')
            
            else:
        """



        return wells

    def _create_pads(self, data):
        self.object_id = 100000
        pads = []
        pad_names = data['Куст'].unique()
        for name in pad_names:
            data_temp = data.loc[data['Куст'] == name].to_numpy()

            pad = PadBuilder(
                format_reader=self.format_reader,
                data=data_temp).build_object()
            self.object_id += 1
            self.object_list[self.object_id] = ObjectRecord.create(object=pad,
                                                                   type_of_object='Pad')
            pads.append(pad)
        return pads

    def _create_clusters(self, data):
        self.object_id = 200000
        clusters = []
        pad_names = data['Название ДНС'].unique()
        for name in pad_names:
            data_temp = data.loc[data['Название ДНС'] == name].to_numpy()
            cluster = ClusterBuilder(
                format_reader=self.format_reader,
                data=data_temp).build_object()
            self.object_id += 1
            self.object_list[self.object_id] = ObjectRecord.create(object=cluster,
                                                                   type_of_object='Cluster')
            clusters.append(cluster)
        return clusters

    def _create_links(self):
        for object_record in self.object_list.values():
            link = self._find_objects(object_record)
            object_record.object.link = link


    def _find_objects(self, object_record: ObjectRecord) -> list:
        link = []
        link_list = object_record.object.object_info.link_list
        type_of_object = object_record.type_of_object
        for key in link_list:
            if key != type_of_object:
                for value in link_list[key]:
                    for base_object in self.object_list.values():
                        if base_object.name[0] == value:
                            link.append(object_record.object)
                            break

        return link
