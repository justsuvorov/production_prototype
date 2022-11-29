from BaseObject.Parser import Parser
import pandas

from BaseObject.ObjectStatus import ObjectStatus
from BaseObject.Indicators import Indicators
from BaseObject.ObjectInfo import ObjectInfo
from BaseObject.Sensor import Sensor
from BaseObject.Hierarchy import Hierarchy

from DomainModel.WellDO import WellDO
from DomainModel.PadDO import PadDO
from DomainModel.Cluster import ClusterDO

from constants import MERNames, StringConstants

from DomainModel.ObjectList import ObjectRecord


class DomainModel:
    def __init__(self,
                 parser: Parser,
                 ):
        self.parser = parser
        self.object_list = {}
        self.object_id = 0

    def create_domain_objects(self):

        wells = self._wells_collection()
        self.object_id = 100000
        pads =self._pads_collection(wells=wells)
        domain_objects = {'Wells': wells, 'Pads': pads}

        return domain_objects

    def _parsed_data(self):
        return self.parser.data()
    def well(self, name: str):
        pass
    def _wells_collection(self):
        wells = {}
        wellsdata = self.wellsdata()
        for well in wellsdata:
            try:
                well_object = self._well_constructor(well)
            except:
                well_object = self._default_well(well)
            finally:
                wells[well[MERNames.WELL][0]] = well_object
                self.object_id += 1
                self.object_list[self.object_id] = self._create_record(object=well_object,
                                                    type_of_object='Well',
                )

        return wells
    def _pads_collection(self, wells: dict):
        pads = {}
        pads_keys = []
        for key in wells:
            if wells[key].object_info.link != []:
                well = wells[key]
                pads_keys.append(well.object_info.link)

        pads_keys_unique = []
        pads_count = 0
        for i in pads_keys:
            if i not in pads_keys_unique:
                pads_keys_unique.append(i)
                pads_count += 1
        for i in range(pads_count):
            pads[pads_keys_unique[i][0]] = PadDO(
                                                name=pads_keys_unique[i][0],
                                                sensor=Sensor(),
                                                object_info=ObjectInfo(objectStatus=ObjectStatus()),
                                                indicators={'No': 'No'},
                                                object_status=ObjectStatus(),
                                                )
            self.object_id += 1
            self.object_list[self.object_id] = self._create_record(object=pads[pads_keys_unique[i][0]],
                                                                   type_of_object='Pad')
        return pads
    def wellsdata(self):
        data = self._parsed_data()
        wellsdata = []
        for _ in data:
            wells_id_list = _[MERNames.WELL].unique()
            for i in range(len(wells_id_list)):
                wellsdata.append(_.loc[[wells_id_list[i]]])
        return wellsdata
    def _field_list(self):
        return self.merData.data_list()
    def _mer(self):
        return self.merData.dataframe()
    def _indicator(self, welldata: pandas.DataFrame):
        return {MERNames.OIL_PRODUCTION: welldata[MERNames.OIL_PRODUCTION]}
    def _well_constructor(self, well: pandas.DataFrame):
        name = well[MERNames.WELL][0]
        link = []

        pad_name = self._find_pad_name(well)
        if pad_name != []:
            link.append(pad_name[0])


        objectInfo = ObjectInfo(link=link, objectStatus=ObjectStatus())
        wellStatus = ObjectStatus()
        #indicators = self._indicator(well)
        indicators = {'Indicators': 'No data'}

        sensor = Sensor()
        return WellDO(name=name,
                    object_info= objectInfo,
                    indicators=indicators,
                    object_status=wellStatus,
                    sensor=sensor)
    def _default_well(self, well: pandas.DataFrame):
        name = well[MERNames.WELL][0]
        objectInfo = ObjectInfo(objectStatus=ObjectStatus())
        indicators = {'Indicators': 'No data'},
        wellStatus = ObjectStatus()
        sensor = Sensor(False)
        return WellDO(name=name,
                    object_info=objectInfo,
                    indicators=indicators,
                    object_status=wellStatus,
                    sensor=sensor
                      )
    def _create_record(self, object, type_of_object: str):
        return ObjectRecord(name=object.name,
                                                    type_of_object=type_of_object,
                                                    object=object,
                                                    links=[],
                                                    status=object.sensor)
    def _find_pad_name(self, well: pandas.DataFrame):
        pad_names = list(well['Куст'].unique())

        pad_names.pop(0)

        return pad_names