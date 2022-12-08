from DomainModel.DomainModel import DomainModel
from Well.MerData import MerData
from ObjectBuilders.Parser import MerParser
from pathlib import Path

DATA_DIR = Path(r'C:\Users\User\Documents\production_prototype\Input\TestData')
#DATA_PATH = DATA_DIR / 'Ямал_БД+Закачка+ГТМ_КПРА_2021.xlsx'

filePath = DATA_DIR/'МЭР_Новопортовское.xlsx'


mer = MerData(dataPath=DATA_DIR)
domainModel = DomainModel(parser=MerParser(merData=mer))
print(domainModel.create_domain_objects())
print(domainModel.object_list)