import datetime as dt
from pathlib import Path
from Tatyana_Prod.calculator import Calculator, \
                    OilPredictionMethod, \
                    FluidPredictionMethod, \
                    WCPredictionMethod


BASE_DIR = Path(__file__).resolve().parent

#ЯМАЛ
MOCK_DATA = BASE_DIR / 'Input'
DATA_DIR = MOCK_DATA
MER_FILES = [MOCK_DATA /'МЭР_Новопортовское.xlsx']
DATA_PATH = [MOCK_DATA / 'Ямал_БД+Закачка+ГТМ_КПРА_2021.xlsx']
HIERARCHY = MOCK_DATA /'Hierarchy.xlsx'
PATH_MACRO = MOCK_DATA/'Макра_model_v21__11.04.2022_обн.СУ22.2Б____22_факт_2021_ОПЕР_с 0 НДПИ — копия.xlsx'
PATH_MASTER = [MOCK_DATA/'МК_Ямал.xlsx']
UNIT_PATH = MOCK_DATA/'Удельные_затраты_БП2022_корр v4.xlsx'
SUBORGS_MAPPING = MOCK_DATA /  'Список_ДО.xlsx'
ARF_FILES = MOCK_DATA/'АРФ_Ямал.xlsx'
MER_TEST_NAME = 'Новопортовское'
TERRA_TEST_NAME = 'ООО "ГПН-Ямал"'
TEST_SUBORG = 'ООО "ГПН - Ямал"'

#DATA_DIR = Path(r'D:\terra\input_portu')
#DATA_PATH = DATA_DIR / 'Ямал_БД+Закачка+ГТМ_КПРА_2021.xlsx'
CUT_DATE = dt.datetime(2019, 1, 1)
START_DATE = dt.datetime(2021, 12, 1)
END_DATE = dt.datetime(2022, 12, 1)



def main():
    """Запуск из командной консоли."""
    calc = Calculator.load(
        data_base_prod=DATA_PATH,
        data_mer=DATA_DIR,
        input_date=START_DATE,
        end_date=END_DATE,
    )
    calc.run(
        oil_method= OilPredictionMethod.WC,
        fluid_method= FluidPredictionMethod.ARPS,
        watercut_method= WCPredictionMethod.COREY,
        start_date=START_DATE,
        cut_date=CUT_DATE,
        account_condensate=True,
        mean_use_coef=True,
        binding_to_mean=True,
    ).save()

if __name__ == '__main__':
    main()
