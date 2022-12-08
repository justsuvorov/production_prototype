from Well.MerData import MerData
from ObjectBuilders.Parser import MerParser
from pathlib import Path
from ObjectBuilders.Builders import *
from ObjectBuilders.FormatReader import *

DATA_DIR = Path(r'C:\Users\User\Documents\production_prototype\Input\TestData')
#DATA_PATH = DATA_DIR / 'Ямал_БД+Закачка+ГТМ_КПРА_2021.xlsx'

filePath = DATA_DIR/'МЭР_Новопортовское.xlsx'
mer = MerData(dataPath=DATA_DIR)
domainModel = DomainModelBuilder(parser=MerParser(merData=mer),
                                 format_reader=MerFormatReader(),
                                 )
do = domainModel.build_object()
print(do)
