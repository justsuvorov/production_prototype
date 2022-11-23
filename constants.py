import numpy as np
from io import BytesIO
from datetime import datetime
from typing import Dict, Union
from pathlib import Path

import pandas as pd



HOURS_IN_DAY = 24
DAYS_IN_YEAR = 365
MONTHS_IN_YEAR = 12

AVG_DAYS_IN_YEAR = 365.2425
AVG_DAYS_IN_MONTH = AVG_DAYS_IN_YEAR / MONTHS_IN_YEAR
INF_COLUMNS_NUMBER = 2
NUMBER_OF_PROD_TYPES = 4
TFileInput = Union[Path, str, Dict[str, Dict], BytesIO]

FIRST_OIL_DATE = pd.Timestamp('1960-01-01 00:00:00')


class StringConstants:
    FIELD = 'Месторождение'
    WELL = '№ скв.'
    LAYER = 'Пласт'
    SUBORGANIZATION = 'ДО'
    WELLS_GROUP = 'Куст'
    PREPARATION_OBJECT = 'Объект подготовки'
    TOTAL = 'Итого'
    DATE = 'Дата'
    OIL_PRODUCTION = 'Добыча нефти'
    LIQUID_PRODUCTION = 'Добыча жидкости'
    PUMPING = 'Закачка, тыс.м3'
    GENERAL_INJECTION = 'Общая закачка'
    AVERAGE_OPERATING_FUND = 'СДФ доб. скважин, шт.'
    OPERATING_FACTOR = 'КЭ доб. скважин, д.ед.'
    GAS_PRODUCTION = 'Добыча ПНГ, млн.м3'
    OPERATING_FUND_MONTH = 'Действующий фонд доб. скважин на конец периода, шт.'
    WELLS_IN_MONTH = 'Прибытие доб скважин, скв'
    WELLS_OUT_MONTH = 'Выбытие доб. скважин, скв'
    WELLS_OUT_PPD = 'Перевод доб. скважин в ППД, скв.'
    WELLS_OUT_UNUSED = 'Выбытие доб. скважин в бездействие, скв.'
    WELLS_OUT_ZBS = 'Выбытие под ЗБС, шт.'
    WELLS_OUT_TO_RETURN = 'Выбытие под ВОЗВРАТ, шт.'
    WELL_TYPE_OIL = 'неф'
    WELL_TYPE_INJ = 'наг'
    FUND_STATE_WORK = 'раб.'
    FUND_STATE_STOP = 'ост.'
    NONAME = 'Noname'
    DEFAULT_OUTPUT_PREFIX = '_OUTPUT'
    DEFAULT_OUTPUT_JSON_PREFIX = 'DATA_FOR_GRAPHS'
    EXTENSION = '.xlsx'
    EXTENSION_JSON = '.json'
    ACCUMULATE_TIME = 'accumulate_time'
    FICTITIOUS_WELLS = 'Фиктивные скважины'
    FICTITIOUS_PREPARATION_OBJECT = 'Фиктивная_ДНС_'
    UEP = 'БРД'  # блок разведки и добычи
    VALUE = 'value'
    KEY = 'key'
    SUM = 'sum'
    CUMULATIVE_TIME = 'CumulativeTime'
    INJECTION = 'Закачка агента, м3 за месяц'
    TERRA_FILE = 'Терра'
    UNNAMED = 'Unnamed'
    TERRA_DATA = 'terra'
    MER_DATA = 'mer'
    PRODUCT = 'Product'
    PICKLE_FOR_SUMMATOR = 'Data_for_summator'
    MONTHLY_INDICATORS = 'MonthlyIndicators'
    GTM = 'gtm'


class Uniqueness:
    SUBORG_FIELD = [StringConstants.SUBORGANIZATION, StringConstants.FIELD]
    SUBORG_FIELD_WELL = [StringConstants.SUBORGANIZATION, StringConstants.FIELD, StringConstants.WELL]
    WELL_LAYER_DATE = [StringConstants.WELL, StringConstants.LAYER, StringConstants.DATE]
    WELL_DATE = [StringConstants.WELL, StringConstants.DATE]
    WELL_LAYER = [StringConstants.WELL, StringConstants.LAYER]


class MetricSIPrefix:
    KILO = 1e3
    MEGA = 1e6


class MERNames:
    MER_FILE = 'МЭР'
    MER_SHEET = 'Анализ'
    WELL = 'Скважинa'
    LAYER = StringConstants.LAYER
    DATE = StringConstants.DATE
    WELL_TYPE = 'Характер работы скважины'
    OPERATING_TIME_HPM = 'Вpемя работы, час за месяц'
    OIL_PRODUCTION = 'Добыча нефти, т за месяц'
    CONDENSATE_OIL_PRODUCTION = 'Добыча газового конденсата (из совм. скважин), т за месяц'
    GAS_PRODUCTION_FROM_GAS_CAP = 'Добыча газа из г/шапки (из совм. скважин), м3 за месяц'
    LIQUID_PRODUCTION = 'Добыча жидкости, т за месяц'
    GAS_PRODUCTION = 'Добыча газа попутного, м3 за месяц'
    SUFFIX = '_MER'
    DOWNTIME = 'Вpемя простоя, час за месяц'
    DATE_STOP = 'Дата остановки скважины'
    DATE_TRANSITION = 'Дата перехода в состояние на конец месяца'
    END_MONTH_STATE = 'Состояние на конец месяца'
    OPERATING_OIL_WELLS = 'Действующие нефтяные'
    SUBORG_NAME = 'Объединение, принявшее скважину'
    PRODUCTION_GAS_CAP = 'Добыча газа из г/шапки (из совм. скважин), м3 за месяц'


    STR_NAMES = [WELL, LAYER, WELL_TYPE, DATE]
    FLOAT_NAMES = [OPERATING_TIME_HPM, OIL_PRODUCTION, LIQUID_PRODUCTION]


class GTMNames:
    GTM_SHEET = 'ГТМ'
    FIELD = StringConstants.FIELD
    WELL = 'скв.'
    LAYER = StringConstants.LAYER
    GTM_KIND = 'Вид ГТМ'
    DATE_START = 'Дата запуска'
    INDICATOR = 'Показатель'
    OPERATING_TIME_PROD_WELLS_DAYS = 'Время работы доб. скважин, сут'
    SUFFIX = '_GTM'
    GAS_PRODUCTION = StringConstants.GAS_PRODUCTION
    OIL_PRODUCTION = 'Добыча нефти, тыс.т'
    GAS_FACTOR = 'Газовый фактор ПНГ, м3/т'
    GTM = 'gtm'

    STR_NAMES = [FIELD, WELL, LAYER, GTM_KIND, INDICATOR]


class OISNames:
    OIS_FILE = 'СПСКВ'
    WELL = 'Скважина'
    LAYER = 'Пласт'
    WELL_TYPE = 'Характер работы'
    FUND_STATE = 'Состояние по фонду'

    STR_NAMES = [WELL, LAYER]


class ColumnNames(GTMNames, MERNames):
    """
    Используемые имена столбцов датафрейма.
    """
    USE_COLUMNS_FOR_MER_RU = [MERNames.DATE, MERNames.LAYER, MERNames.WELL, MERNames.WELL_TYPE,
                              MERNames.DATE_STOP, MERNames.OIL_PRODUCTION,
                              MERNames.LIQUID_PRODUCTION, MERNames.OPERATING_TIME_HPM,
                              MERNames.DOWNTIME, MERNames.GAS_PRODUCTION]
    USE_COLUMNS_FOR_MER_EN = ['Date', 'Layer', 'WellName', 'WellType', 'DateStop', 'OilProduction',
                              'LiquidProduction', 'OperatingTimeHPM', 'DowntimeHPM', 'GasProduction']
    USE_COLUMNS_FOR_GTM_RU = [GTMNames.FIELD, GTMNames.WELL, GTMNames.LAYER, GTMNames.DATE_START,
                              GTMNames.GTM_KIND, GTMNames.INDICATOR]
    USE_COLUMNS_FOR_GTM_EN = ['FieldName', 'WellName', 'Layer', 'LaunchDate', 'GtmKind', 'Indicator']
    USE_COLUMNS_FOR_SUBORG = ['№ п.п.', 'Родительский ОП', 'Ед.изм.', 'Итого']

    MER_COLUMNS_TRANSLATION = dict(zip(USE_COLUMNS_FOR_MER_EN, USE_COLUMNS_FOR_MER_RU))
    GTM_COLUMNS_TRANSLATION = dict(zip(USE_COLUMNS_FOR_GTM_EN, USE_COLUMNS_FOR_GTM_RU))

    OF_INDICATORS = {
        'OperatingFundMonth': StringConstants.OPERATING_FUND_MONTH,
        'WellsIn': StringConstants.WELLS_IN_MONTH,
        'WellsOut': StringConstants.WELLS_OUT_MONTH,
        'WellsOutPPD': StringConstants.WELLS_OUT_PPD,
        'WellsOutUnused': StringConstants.WELLS_OUT_UNUSED,
        'WellsOutZBS': StringConstants.WELLS_OUT_ZBS,
        'WellsOutToReturn': StringConstants.WELLS_OUT_TO_RETURN
    }


class ProductionNames:
    BaseProd: str
    MER: str
    Code: str
    StandardCode: str


class OilProductionNames(ProductionNames):
    BaseProd = GTMNames.OIL_PRODUCTION
    MER = MERNames.OIL_PRODUCTION
    Code = 'Добыча нефти'
    StandardCode = StringConstants.OIL_PRODUCTION


class LiquidProductionNames(ProductionNames):
    BaseProd = 'Добыча жидкости, тыс.т'
    MER = MERNames.LIQUID_PRODUCTION
    Code = 'Добыча жидкости'
    StandardCode = StringConstants.LIQUID_PRODUCTION


class GasProductionNames(ProductionNames):
    BaseProd = StringConstants.GAS_PRODUCTION
    MER = MERNames.GAS_PRODUCTION
    Code = 'Добыча газа'
    StandardCode = StringConstants.GAS_PRODUCTION


class DatetimeFormat:
    InputDate = '%d.%m.%Y'
    FileDate = '%Y-%m-%d %H:%M:%S'
    OutputDate = 'DD.MM.YYYY'


class ConstantsForCalc:
    NMONTHFORGTM = 8  # Количество месяцев для нахождения ГТМов
    BOUND = ((0.00001, 50), (0.00001, 0.999), (0.00001, 0.999), (5, 100))  # Левые и правые границы параметров кривой Арпса
    START_POINT_FOR_CURVE_ARPS = np.array([0.737052938, 0.999, 0.020762861, 5.5])  # Стартовая точка для нахождения коэффициентов кривой Арпса
    PART_OIL_PROD = 1 / 5
    N_MONTH_FOR_PREDICT_GAS = 6
    SEARCH_BOX = 3
    NUMBER_SMOOTHINGS = 7 # Количество сглаживаний скользящим средним
    DEFAULT_OPERATING_FACTOR = 0.95
    MIN_MONTHS_FOR_ARPS = 3


class CurveNames:
    SIPACHEV_POSEVISH = 'Сипачёв-Посевич'
    NAZAROV_SIPACHEV = 'модификация Назаров-Сипачёв'
    SAZONOV = 'Сазонов'
    MOVMYGA_CHEREPACHIN = 'Мовмыга-Черепахин'
    ABYZBAEV = 'Абызбаев'
    KAMBAROV = 'Камбаров'


class FluidConstans:
    SHIFT = 1  # смещение
    PERIOD_ADAPT = 2 / 3  # коэффициент выбора адаптивного периода
    START_POINT_A = 0.2  # начальный коэффициент для выбора участка адаптация+ретро
    LEAST_MONTHS = 18  # предельное количество месяцев в периоде адаптация+ретро
    EXTREME_DIFFERENCE = 10  # предельное значения отклонения по DELTA
    REDUCTION_RATIO = 0.9  # коэффициент уменьшения для участка кривод для адаптации+ретро
    EXTREME_ADAPTATION = 18  # предельное количество месяцев для периода адаптации
    USING_WATER_CUT = 0.5  # обводнённость пласта при которой допустимо использовать характеристики обводнения
    OVERLAP = 20  # число месяцев пересечения месяцев факта с прогнозными. Требуется для корректного прогноза.
    DOWN_BORDER = -10000000  # нижняя граница коэффициента для вычисления ХВ по функции "Мовмыги-Черепахи"
    TOP_BORDER = 10000000  # верхняя граница коэффициента для вычисления ХВ по функции "Мовмыги-Черепахи"
    MAX_FEV = 300000
    N_MEAN = 7  # количество периодов по которым берётся среднеарифмитеческое
    MAX_WC_FOR_LOW_WC_LAYERS = 0.6 # Максимальная обводненность для низвообводненных пластов
    DEFAULT_BINDING_PERIOD = 3


class FluidFunc:
    METHODS = {
        CurveNames.SIPACHEV_POSEVISH: lambda x, a, b: a * x / (1 - b * x),
        CurveNames.NAZAROV_SIPACHEV: lambda x, a, b: x * (1 + np.exp(a + b * x)),
        CurveNames.SAZONOV: lambda x, a, b: x * (1 + np.exp(a + b * np.log(x))),
        CurveNames.MOVMYGA_CHEREPACHIN: lambda x, a, b: (1 / b) * np.log(a / (a - b * x) + x),
        CurveNames.ABYZBAEV: lambda x, a, b: np.exp(np.log((x - a) / b)),
        CurveNames.KAMBAROV: lambda x, a, b: b / (x - a)
    }


class ConstForGraphs:
    """Константы, используемые в тестах на проверку контракта данных."""
    META = 'meta'
    DATA = 'data'
    GROUP = 'group'
    VALUES = 'values'
    PARENT = 'parent'
    RESOURCE = 'resource'
    TYPE = 'type'
    GRANULARITY = 'granularity'

    MAIN_KEYS = [META, DATA]
    INTERNAL_KEYS = [GROUP, VALUES, PARENT, RESOURCE, TYPE, GRANULARITY]


class FundFormationDates:

    fund_formation_excluded = {'ООО "ГПН-Восток"': datetime(2017, 1, 1)}
    BASE_FUND = datetime(2020, 1, 1)
    SUBORG_MAPPING = {
    'Восток': 'ООО "ГПН-Восток"',
    'Мессояха': 'АО «Мессояханефтегаз»',
    'ННГ': 'AO «ГПН-ННГ»',
    'Оренбург': 'ООО "ГПН-Оренбург"',
    'Славнефть': 'ПАО_СН_МНГ',
    'Хантос': 'ООО "ГПН-Хантос"',
    'Ямал': 'ООО "ГПН - Ямал"'
    }

class CumulativeConstansts:

    SUBORG = StringConstants.SUBORGANIZATION
    FIELD = StringConstants.FIELD
    OIL_PRODUCTION_BASE_FUND= 'Накопленная добыча нефти по БД, тыс т'
    OIL_PRODUCTION_GTM = 'Накопленная добыча нефти по ГТМ (01.20-02.22), тыс т'
    SUM_OIL_PRODUCTION = 'Накопленная добыча нефти по БД+ГТМ, тыс т'




class FormationBase:
    MONTH_ARRIVE = 'Месяц прибытия'
    MONTH_CUT = 'Месяц выбытия'
    OIL_FUND_ARR = 'Нефтяной_фонд_прибытие'
    OIL_FUND_CUT = 'Нефтяной_фонд_выбытие'
    GTM_BF = 'ГТМ/БФ'
    BF = 'БФ'
