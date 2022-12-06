from abc import ABC
import pandas as pd
from constants import MERNames, StringConstants
from BaseObject.ObjectInfo import ObjectInfo

class FormatReader(ABC):

    def names(self, df: pd.DataFrame) -> dict:
        pass

    def _object_type(self,  df: pd.DataFrame) -> list:
        pass

    def object_info(self, df: pd.DataFrame) -> ObjectInfo:
        pass

    def indicators(self, df: pd.DataFrame) -> dict:
        pass


class MerFormatReader(FormatReader):

    def __init__(self,
                 indicator_names: list = None):
        self.indicator_names = indicator_names

    def names(self, df: pd.DataFrame):
        try:
            well_name = df[MERNames.WELL]
            pad_name = df['Куст']
            field = df['Месторождение']

        except:
            print('Corrupted date')
            well_name = 'Noname'
            pad_name = 'Noname'
            field = 'Noname'

        finally:
            return {'Well': well_name, 'Куст': pad_name, 'Месторождение': field}

    def _object_type(self, df: pd.DataFrame):
        return df['Характер работы скважины'].tolist()

    def indicators(self, df: pd.DataFrame):
        result = {}
        for _ in self.indicator_names:
            result[_] = df[_]
        return result

    def object_info(self, df: pd.DataFrame) -> ObjectInfo:
        return ObjectInfo(
            object_type=self._object_type(df),
            link=[df['Куст'].unique[0], df['Месторождение'].unique()[0]]
        )
