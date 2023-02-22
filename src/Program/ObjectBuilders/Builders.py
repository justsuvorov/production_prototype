import pandas as pd
import numpy as np

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
from Program.DomainModel.FieldDO import FieldDO


class WellBuilder(BaseObjectBuilder):

    def __init__(self,
                 format_reader: FormatReader,
                 data: np.array):
        self.format_reader = format_reader
        super().__init__(format_reader=format_reader)
        self.data = data

    def build_object(self) -> Object:

       return WellDO(
           name=self.format_reader.names(self.data)['Well'],
           object_info=self._object_info(),
           indicators=self._indicators(),
           sensor=self.sensor(),
           link={}
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
                 data: np.array
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
                 data: np.array,
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
            link={}
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


class FieldBuilder(BaseObjectBuilder):

    def __init__(self,
                 format_reader: FormatReader,
                 data: np.array,
                 ):
        self.format_reader = format_reader
        self.data = data
        super().__init__(format_reader=format_reader)

    def build_object(self) -> Object:
        return FieldDO(
            name=self.format_reader.names(self.data)['Field'],
            object_info=self._object_info(),
            indicators=self._indicators(),
            sensor=self.sensor(),
            link={}
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
        if only_wells is False or None:
           # domain_model.append(self._create_pads(data))
            domain_model.append(self._create_clusters(data))
            domain_model.append(self._create_fields(data))

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
            self.object_list[str(well.name[0])+str(well.object_info.link_list['Field'][0])] =\
                ObjectRecord.create(object=well, type_of_object='Well')

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
            self.object_list[str(cluster.name[0])] = ObjectRecord.create(object=cluster,
                                                                         type_of_object='Cluster')
            clusters.append(cluster)

        for cluster in clusters:
            cluster.link['Wells'] = []
            for i in range(len(cluster.object_info.link_list['Field'])):
                wells_names = cluster.object_info.link_list['Well']+cluster.object_info.link_list['Field'][i]
                for well in wells_names:
                    if well in self.object_list.keys():
                        cluster.link['Wells'].append(self.object_list[well].object)
                        self.object_list[well].object.link['Clusters'] = []
                        self.object_list[well].object.link['Clusters'].append(cluster)

        return clusters

    def _create_fields(self, data):
        self.object_id = 200000
        fields = []
        field_names = data['Месторождение'].unique()
        for name in field_names:
            data_temp = data.loc[data['Месторождение'] == name].to_numpy()
            field = FieldBuilder(
                format_reader=self.format_reader,
                data=data_temp).build_object()
            self.object_id += 1
            self.object_list[str(field.name[0])] = ObjectRecord.create(object=field,
                                                                         type_of_object='Field')
            fields.append(field)

        for field in fields:
            field.link['Wells'] = []
            for i in range(len(field.object_info.link_list['Field'])):
                wells_names = field.object_info.link_list['Well']+field.object_info.link_list['Field'][i]
                for well in wells_names:
                    if well in self.object_list.keys():
                        field.link['Wells'].append(self.object_list[well].object)
                        self.object_list[well].object.link['Fields'] = []
                        self.object_list[well].object.link['Fields'].append(field)

        return fields

    @staticmethod
    def merge_objects(clusters):
        new_clusters = {}
        temp1 = 0
        for object in clusters:
            temp1 += len(object.link['Wells'])
            if str(object.name[0]) not in new_clusters.keys():
                new_clusters[str(object.name[0])] = object
            else:
                new_clusters[str(object.name[0])].link['Wells'] += object.link['Wells']
        temp2 = 0
        for key in new_clusters:
            temp2 += len(new_clusters[key].link['Wells'])

        return list(new_clusters.values())