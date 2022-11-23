#from MerData import MerData
import pandas

from Well.WellInfo import WellInfo, ObjectInfo
from constants import MERNames, StringConstants
from Well.MerData import MerData
#from ObjectStatus import ObjectStatus
from Well.Well import Well

from Well.WellStatus import WellStatus
from Well.Sensor import Sensor


class WellFromMer:
    def __init__(self,
                 merData: MerData
                 ):
        self.merData = merData

    def wells_collection(self):
        Wells = []
        wellsdata = self.wellsdata()
        for well in wellsdata:
            try:
                Wells.append(Well(
                    id=well[MERNames.WELL][0],
                    objectInfo=self._well_info(welldata=well),
                    indicators = self._indicator(well),
                    wellStatus=WellStatus(),
                    sensor=Sensor()
                                )
                )
            except:
                Wells.append(Well(
                    id = 1,
                    objectInfo = self._well_info(welldata=well),
                    indicators = {'Indicators': 'No data'},
                    wellStatus = WellStatus(),
                    sensor = Sensor(False)
                                )
                )
        return Wells



    def wellsdata(self):
        data = self._mer()
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
        return  { MERNames.OIL_PRODUCTION: welldata[MERNames.OIL_PRODUCTION]}


