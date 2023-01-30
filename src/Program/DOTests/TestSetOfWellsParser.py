from Program.ObjectBuilders.Parser import SetOfWellsParser
from pathlib import Path
import pandas as pd
DATA_DIR = Path(r'C:\Users\User\Documents\production_prototype\Input\TestData')
#DATA_PATH = DATA_DIR / 'Ямал_БД+Закачка+ГТМ_КПРА_2021.xlsx'

filePath = DATA_DIR/'СВОД_скв._NEW_5лет.xlsx'
pd.options.display.max_columns = 300

data = SetOfWellsParser(data_path=filePath).data().head().to_numpy()

print(data[0])


