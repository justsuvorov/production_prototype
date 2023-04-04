import os
from glob import glob
from pathlib import Path

import pandas as pd

from Program.ObjectBuilders.Builders import *
from Program.ObjectBuilders.FormatReader import SetOfWellsFormatReader
from Program.ObjectBuilders.Parser import SetOfWellsParser
from Program.constants import DATA_DIR

VBD_DIR = Path(r'C:\Users\User\Documents\production_prototype\Input\TestData\VBD')

# DATA_DIR = Path(r'C:\Users\User\Documents\production_prototype\Input\ProductionTests')
vbd_pathes = [y for x in os.walk(VBD_DIR) for y in glob(os.path.join(x[0], '*.xls*'))]
filePath = DATA_DIR / 'СВОД_скв._NEW_5лет.xlsx'
vbd = DATA_DIR / 'VBD.xlsx'

"""
def prepare_data(pathes_list):
    data = []
    for i in range(len(pathes_list)):
        df = pd.read_excel(pathes_list[i])
        data.append(df.loc[1:])
    resdata = data[0]
    for i in range(len(pathes_list) - 1):
        resdata = pd.concat([resdata, data[i + 1]])
    resdata.to_excel('VBD.xlsx')
    return 'VBD_ranged.xlsx'
"""
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

def domain_model(file_path):

    filePath = file_path / 'СВОД_скв._NEW_5лет.xlsm'
   # vbd_initial = file_path / 'VBD.xlsm'
    #vbd = prepare_data(file_path=file_path)
    print('Прочитан xlsm формат')
#    vbd = prepare_data(file_path=file_path)



    domain_model = DomainModelBuilder(parser=SetOfWellsParser(data_path=filePath),
                                      format_reader=SetOfWellsFormatReader(),
                                      ).build_object(only_wells=False)

    vbd_domain_model = DomainModelBuilder(parser=SetOfWellsParser(data_path=vbd),
                                          format_reader=SetOfWellsFormatReader(),
                                          ).build_object(only_wells=False)
    for object in vbd_domain_model[0]:
        object.change_activity()

    domain_model_full_wells = domain_model[0] + vbd_domain_model[0]
    #domain_model_full_pads = domain_model[1]+vbd_domain_model[1]
    domain_model_full_clusters = domain_model[1]+vbd_domain_model[1]
    domain_model_full_fields = domain_model[2] + vbd_domain_model[2]
    result_domain_model = []
    result_domain_model.append(domain_model_full_wells)
    # result_domain_model.append(domain_model_full_pads)
    clusters = DomainModelBuilder.merge_objects(domain_model_full_clusters)
    fields = DomainModelBuilder.merge_objects(domain_model_full_fields)
    result_domain_model.append(clusters)
    result_domain_model.append(fields)


    return result_domain_model
