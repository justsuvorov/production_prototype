import pandas as pd

from Program.Well.MerData import MerData


# from MerData import MerData
#from ObjectStatus import ObjectStatus

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
        return pd.read_excel(self.data_path).loc[1:]


class GfemParser(Parser):
    def __init__(self,
                 data_path: str,
                 ):
        self.data_path = data_path

    def data(self) -> pd.DataFrame:
        return pd.read_excel(self.data_path,)[['Месторождение','Скважина', 'Куст', 'FCF первый месяц:','НДН за первый месяц; тыс. т']]


class PortuResultsParser(Parser):
    def __init__(self,
                 data_path: str,
                 ):
        self.data_path = data_path

    def data(self) -> dict:
        return pd.read_excel(self.data_path, None)
