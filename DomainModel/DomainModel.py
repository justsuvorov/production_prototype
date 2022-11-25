from BaseObject.Parser import Parser
import pandas

from BaseObject.ObjectStatus import ObjectStatus
from BaseObject.Indicators import Indicators
from BaseObject.ObjectInfo import ObjectInfo
from BaseObject.Sensor import Sensor

from DomainModel.WellDO import WellDO
from constants import MERNames, StringConstants

from DomainModel.ObjectList import ObjectRecord


class DomainModel:
    def __init__(self,
                 parser: Parser,
                 ):
        self.parser = parser
        self.object_list = {}
        self.object_id = 1

    def create_domain_objects(self):
        domain_objects = {}
        wells = self.wells_collection()
        domain_objects

        return

    def _parsed_data(self):
        return self.parser.data()

    def well(self, name: str):
        pass
    def wells_collection(self):
        wells = {}
        wellsdata = self.wellsdata()
        for well in wellsdata:
            try:
                name=well[MERNames.WELL][0]
                objectInfo=self._well_info(welldata=well)
                indicators=self._indicator(well)
                wellStatus=ObjectStatus()
                sensor=Sensor()

            except:
                name=well[MERNames.WELL][0]
                objectInfo=self._well_info(welldata=well),
                indicators={'Indicators': 'No data'},
                wellStatus=ObjectStatus(),
                sensor=Sensor(False)

            finally:
                wells[well[MERNames.WELL][0]] = WellDO(name=name,
                                                    object_info= objectInfo,
                                                    indicators=indicators,
                                                    object_status=wellStatus,
                                                    sensor=sensor
                                                       )
                self.object_id += 1
                self.object_list[self.object_id] = ObjectRecord(
                                                    name=well[MERNames.WELL][0],
                                                    type_of_object='Well',
                                                    object=wells[well[MERNames.WELL][0]],
                                                    links = [],
                                                    status = sensor
                )

        return wells

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

    def _well_info(self, welldata: pandas.DataFrame):
        plastInfo = welldata[MERNames.LAYER].unique()
        wellType = welldata[MERNames.WELL_TYPE].unique()
        status = welldata[MERNames.LAYER].unique()
        linkList = {
            'Скважина': welldata[MERNames.WELL].unique(),
            'Куст': welldata['Куст'].unique(),
            'ДНС': welldata['Объект сбора ДНС (по справ)'].unique(),
            'Месторождение': welldata[StringConstants.FIELD].unique(),
            'Лицензионный участок': welldata['Лицензионный участок'].unique(),
            'ДО': welldata[MERNames.SUBORG_NAME].unique()
        }

        return ObjectInfo(
            linkList=linkList,
            objectStatus=status,
        )

        #            wellType=wellType,
        #             plastInfo=plastInfo,
        #             )

    def _indicator(self, welldata: pandas.DataFrame):
        return {MERNames.OIL_PRODUCTION: welldata[MERNames.OIL_PRODUCTION]}
