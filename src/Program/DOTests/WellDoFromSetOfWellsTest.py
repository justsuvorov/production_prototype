import os
from glob import glob
from pathlib import Path

from Program.ObjectBuilders.Builders import *
from Program.ObjectBuilders.FormatReader import SetOfWellsFormatReader
from Program.ObjectBuilders.Parser import SetOfWellsParser
from Program.constants import DATA_DIR

VBD_DIR = Path(r'C:\Users\User\Documents\production_prototype\Input\TestData\VBD')

# DATA_DIR = Path(r'C:\Users\User\Documents\production_prototype\Input\ProductionTests')
vbd_pathes = [y for x in os.walk(VBD_DIR) for y in glob(os.path.join(x[0], '*.xls*'))]
filePath = DATA_DIR / 'СВОД_скв._NEW_5лет.xlsx'
vbd = DATA_DIR / 'VBD.xlsx'


def prepare_data(pathes_list):
    data = []
    for i in range(len(pathes_list)):
        df = pd.read_excel(pathes_list[i])
        data.append(df.loc[1:])
    resdata = data[0]
    for i in range(len(pathes_list) - 1):
        resdata = pd.concat([resdata, data[i + 1]])
    resdata.to_excel('VBD.xlsx')
    return 'VBD.xlsx'


def domain_model(file_path):

    filePath = file_path / 'СВОД_скв._NEW_5лет.xlsm'
    vbd = file_path / 'VBD.xlsm'
    print('Прочитан xlsm формат')

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
    result_domain_model = []
    result_domain_model.append(domain_model_full_wells)
    # result_domain_model.append(domain_model_full_pads)
    clusters = DomainModelBuilder.merge_clusters(domain_model_full_clusters)
    result_domain_model.append(clusters)

    return result_domain_model
