from abc import ABC

import numpy as np
import pandas as pd

from Program.BaseObject.ObjectInfo import ObjectInfo


class FormatReader(ABC):

    def names(self, df: pd.DataFrame) -> dict:
        pass

    def _object_type(self,  df: pd.DataFrame) -> list:
        pass

    def object_info(self, df: pd.DataFrame) -> ObjectInfo:
        pass

    def indicators(self, df: pd.DataFrame) -> dict:
        pass


class SetOfWellsFormatReader(FormatReader):

    def __init__(self,
                 indicator_names: list = None):
        self.indicator_names = indicator_names
        self.count = 0

    def names(self, df: np.array):
        try:
            well_name = np.unique(df.T[2])
            pad_name = np.unique(df.T[3])
            cluster_name = np.unique(df.T[1])
            field = np.unique(df.T[0])

        except:
            print('Corrupted data', df)

            well_name = 'Noname'
            pad_name = 'Noname'
            cluster_name = 'Noname'
            field = 'Noname'

        finally:
            return {'Well': well_name, 'Pad': pad_name, 'Cluster': cluster_name, 'Field': field}

    def _object_type(self, data: np.array):
        # return df['Характер работы скважины'].tolist()
        return str('неф')

    def _object_activity(self, data: np.array):


       try:
           activity = data.T[184]
           shape = activity.shape
           if shape[0] > 1:
               return True
           if activity == 1:
               return True
           else:
               return False

       except:
                return True








    def indicators(self, data: np.array):
        result = {}
        self.count += 1
        self.indicator_names = ['Добыча нефти, тыс. т', 'Добыча жидкости, тыс. т', 'FCF']
        indicators_numbers = [5, 65, 125, 184]
        indicators_numbers1 = [5, 65, 125]
        j = 0
        if data.shape[0] > 1:
            data = data.T

        else:
            try:
                data = data[0]
            except:
                print('Corrupt Well, string ', self.count)
        for i in indicators_numbers1:
            a = np.arange(i - 1, indicators_numbers[j + 1] - 1)
            result[self.indicator_names[j]] = data[a]
            j += 1
        return result




    def object_info(self, data: np.array, object_list: dict = None) -> ObjectInfo:

        return ObjectInfo(
            object_type=self._object_type(data),
            object_activity=self._object_activity(data),
            link_list=self.names(data),

            #link=self.create_links(object_list)
            #  link=[df['Куст'].unique()[0], df['Месторождение'].unique()[0]]
        )
    def create_links(self, object_list: dict = None):
        pass


class MerFormatReader(FormatReader):

    def __init__(self,
                 indicator_names: list = None):
        self.indicator_names = indicator_names

    def names(self, data: np.array):
        try:
            shape = data.shape[0]
            if shape == 1:
                well_name = data[3]
                pad_name = data[5]
                field = data[1]
            else:
                well_name = data[1][3]
                pad_name = data[1][5]
                field = data[1][1]

        except:
            print('Corrupted date')
            well_name = 'Noname'
            pad_name = 'Noname'
            field = 'Noname'

        finally:
            return {'Well': well_name, 'Куст': pad_name, 'Месторождение': field}

    def _object_type(self, data: np.array):
        #return df['Характер работы скважины'].tolist()
        return data.T[4]

    def indicators(self,  data: np.array):
        result = {}

        self.indicator_names = ['Добыча нефти, тыс. т', 'Добыча жидкости, тыс. т', 'Добыча газа, тыс. т']
        indicators_numbers = [25, 27, 30]
        j = 0
        if data.shape[0] > 1:
            data = data.T
        for i in indicators_numbers:
            result[self.indicator_names[j]] = data[i]
            j += 1

        return result

    def object_info(self, data: np.array) -> ObjectInfo:
        return ObjectInfo(
            object_type=self._object_type(data),
            link=[]
          #  link=[df['Куст'].unique()[0], df['Месторождение'].unique()[0]]
        )