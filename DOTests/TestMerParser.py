from Well.MerData import MerData
from BaseObject.Parser import MerParser
from pathlib import Path

DATA_DIR = Path(r'C:\Users\User\Documents\production_prototype\Input\TestData')
#DATA_PATH = DATA_DIR / 'Ямал_БД+Закачка+ГТМ_КПРА_2021.xlsx'

filePath = DATA_DIR/'МЭР_Новопортовское.xlsx'


mer = MerData(dataPath=DATA_DIR)
#dict_data = mer.data_dict()
#df = mer.dataframe()
#dataList = mer.data_list()
domain = MerParser(merData=mer).data()
print(domain)
