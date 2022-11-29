import pandas as pd
import datareader as DR
from pathlib import Path

class MerData:
    def __init__(self,
                 dataPath: str,
                 ):
        self.data_path = dataPath

    def data_dict(self):
        data = self._read_data()
        return data[0]

    def data_list(self):
        data = self._read_data()
        return data[1]

    def dataframe(self):
        data = self.data_dict()
        dataframes = []
        for key in data:
            dataframes.append(pd.DataFrame(data[key]))

        return dataframes

    def _read_data(self):
        #return DR.find_input_files(self.data_path, self.data_path)
        #return DR.read_mer_from_file(self.data_path)
        if isinstance(self.data_path, (Path, str)) and isinstance(self.data_path, (Path, str)):
            mer_dict, fields = DR.find_input_files(
                self.data_path,
                self.data_path,
            )
        else:
            raise ValueError('Нет корректных данных для расчета')
        return mer_dict, fields