import os
from glob import glob
from pathlib import Path

import pandas as pd

from Program.ObjectBuilders.Builders import *
from Program.ObjectBuilders.FormatReader import *
from Program.ObjectBuilders.Parser import SetOfWellsParser
from Program.constants import DATA_DIR
from Program.Production.PreparedDomainModel import PreparedDomainModel


filePath = DATA_DIR / 'СВОД_скв._NEW_5лет.xlsx'
path = r'C:\Users\User\Documents\production_prototype\src\program\data'

def prepare_data(file_path):
    vbd_initial = file_path / 'VBD.xlsm'
    df_origin = pd.read_excel(vbd_initial)
    df = df_origin.iloc[1:]
    pd.options.mode.chained_assignment = None
    df['FCF'] = df.iloc[:, 125:137].sum(axis=1)
    df['Qsum'] = df.iloc[:, 5:17].sum(axis=1)
    df['FCF/Q'] = df['FCF']/df['Qsum']

    resdata = df.sort_values(by=['FCF/Q'], ascending=False)
    resdata = resdata.shift()

   # self.indicator_names = ['Добыча нефти, тыс. т', 'Добыча жидкости, тыс. т', 'FCF']
   # indicators_numbers = [5, 65, 125, 184]
   # indicators_numbers1 = [5, 65, 125]

    resdata.to_excel(file_path /'VBD_ranged.xlsx', index=False)
    return file_path /'VBD_ranged.xlsx'

def domain_model_from_gfem(file_path):

    wells_file = file_path / 'СВОД_скв._NEW_5лет.xlsm'
    pads_file = file_path / 'СВОД_NEW_куст_5лет.xlsm'
    clusters_file = file_path / 'СВОД_NEW_ДНС_5лет.xlsm'

    print('Прочитан xlsm формат')

    domain_model = IterativeDomainModelBuilder(parser=SetOfWellsParser(data_path=wells_file),
                                               format_reader=SetOfWellsFormatReader(),
                                               ).build_object(only_wells=False)
    clusters = DomainModelBuilder.merge_objects(domain_model[2])
    domain_model[2] = clusters


    return domain_model


if __name__ == '__main__':
    domain_model_from_gfem(file_path=Path(path))