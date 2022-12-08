from abc import ABC
from pathlib import Path

import pandas as pd

from Well.MerData import MerData
#from MerData import MerData
import pandas

from Well.WellInfo import WellInfo, ObjectInfo
from constants import MERNames, StringConstants
from Well.MerData import MerData
#from ObjectStatus import ObjectStatus
from Well.Well import Well

from Well.WellStatus import WellStatus
from Well.Sensor import Sensor

class Parser:

    def data(self) :#-> pd.DataFrame:
        pass

    def gtm_object(self):
        pass

    def domain_model(self):
        pass

class MerParser(Parser):
    def __init__(self,
                 merData: MerData
                 ):
        self.merData = merData

    def data(self) :#-> pd.DataFrame:
        data = self._mer()[0]
        return data

    def _mer(self):
        return self.merData.dataframe()

class SetOfWellsParser(Parser):
    def __init__(self,
                 data_path: str,
                 ):
        self.data_path = data_path

    def data(self) -> pd.DataFrame:
        return pd.read_excel(self.data_path)