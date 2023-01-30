#import warnings
from typing import Dict, List, Tuple
from pathlib import Path
from datetime import datetime, date
import numpy as np
import os
import pandas as pd


from Program.constants import StringConstants as SC, TFileInput
from Program.constants import (
    ColumnNames,
    GTMNames,
    MERNames,
    OISNames,
)
from Program.constants import ConstantsForCalc as Const
from Program.utils.parsers import parse_date
from Program.utils.service import to_numeric




def _get_field_name(data_path: str) -> str:
    """Возвращает имя месторождения.

    :param data_path: путь к файлу.
    :return: имя месторождения
    """
    return normalize(os.path.splitext(data_path)[0][data_path.find('_') + 1:])


def _get_name_suborg(path: Path) -> str:
    """Возвращает имя ДО

    :param path: путь к файлу
    :return: имя ДО
    """
    return os.path.basename(path).split('_').pop(0)


def _read_excel(path: Path, *args, **kwargs):
    """
    Возвращает список листов, пригодных для чтения (убирает листы ChartSheets).

    Принимает:
    - path - строка пути к файлу на диске.
    """
    xlf = pd.ExcelFile(path)
    out = {}

    for sheet in xlf.sheet_names:
        try:
            out[sheet] = xlf.parse(sheet, *args, **kwargs)
        except AttributeError:
            pass
    return out


def normalize(name: str) -> str:
    return name.lower().replace(' ', '')


def read_mer_from_file(data_mer: TFileInput) -> pd.DataFrame:
    """
    Возвращает считанный из файла объект pandas.DataFrame.

    Принимает:
    - data_mer - входные данные для чтения файлов МЭР
    (строка пути к файлу или словарь, содержащий данные листов excel-файла МЭР).
    """
    if isinstance(data_mer, (Path, str)):
        file = _read_excel(data_mer, None)
    else:
        file = data_mer
    sheets = list(file.keys())
    name_sheets = list(filter(lambda x: x.find(MERNames.MER_SHEET) != -1, sheets))
    lists = [0] * len(name_sheets)
    lists[0] = file[name_sheets[0]].loc[6:].reset_index(drop=True)
    for i in range(len(name_sheets) - 1):
        lists[i + 1] = file[name_sheets[i + 1]].loc[2:].reset_index(drop=True)
    df = pd.concat(lists, ignore_index=True)
    df.columns = file[name_sheets[0]].loc[4]
    df[MERNames.STR_NAMES] = df[MERNames.STR_NAMES].astype('string')
    df[SC.DATE] = pd.to_datetime(df[SC.DATE].astype(str), format='%Y/%m')
    df.index = df[MERNames.WELL]
    df.index.name = None
    df[MERNames.FLOAT_NAMES] = to_numeric(df[MERNames.FLOAT_NAMES], axis=0)
    try:
        df = df.astype({MERNames.DATE_STOP: 'datetime64'})
    except (ValueError, TypeError):
        df = df.astype({MERNames.DATE_STOP: 'string'})
    return df


def read_bd_reinj_from_file(
    data: pd.DataFrame,
    end_date: datetime,
    date_analysis: datetime,
    ) -> pd.DataFrame:
    """ Обработка файла с данными о БД и закачке

    :param data: DataFrame с данными о БД и закачке.
    :return: DataFrame с обработанными данными о БД и закачке.
    """
    df = data.copy()
    df = df.loc[:, ~df.columns.str.contains(SC.UNNAMED)]
    df.columns = pd.date_range(
        parse_date(df.columns[0]), periods=len(df.columns), freq='MS'
    )
    inf_data_column = 2 if any(data.iloc[:, 2].isin([GTMNames.OIL_PRODUCTION])) else 3
    df = pd.concat([pd.Series(data=data.iloc[:, inf_data_column], name=SC.FIELD), df], axis=1).fillna(0)
    if end_date:
        #if end_date > df.columns[-1]:
            #warnings.warn('Конечная дата больше, чем максимально возможная дата прогноза. ' +
            #              f'Последняя дата прогноза будет {str(df.columns[-1])}')
        #else:
        bd_df = df[df.columns[1:]]
        cut_df = bd_df[bd_df.columns[bd_df.columns <= end_date]]
        df = pd.concat([df[SC.FIELD], cut_df], axis=1)
    return df


def read_gtm_from_file(gtm_data: pd.DataFrame, all_dates: List[date]) -> pd.DataFrame:
    """
    Возвращает считанный из файла объект pandas.DataFrame.

    Принимает:
    - gtm_data - DataFrame, содержащий данные по ГТМ.
    - all_dates - Список дат для прогноза.
    """
    df = gtm_data.copy()
    name_columns_all = []
    name_columns_see = [
        SC.FIELD,
        GTMNames.WELL,
        GTMNames.LAYER,
        GTMNames.DATE_START,
        GTMNames.GTM_KIND,
        GTMNames.INDICATOR,
    ]
    for i in df.columns:
        try:
            dates = datetime.strptime(str(i), '%d.%m.%Y')
            name_columns_all.append(dates)
            if dates >= min(all_dates) and dates <= max(all_dates):
                name_columns_see.append(dates)
        except ValueError:
            name_columns_all.append(i)
            continue
    df.columns = name_columns_all
    df = df.loc[:, name_columns_see]
    df = df.dropna(subset=[GTMNames.DATE_START]).reset_index(drop=True)
    return df


def read_bd_reinj_gtm_file(
    data_base_prod: TFileInput,
    end_date: datetime,
    date_analysis: datetime,
) -> Tuple[Dict, list]:
    """Возвращает считанный из файла словарь с показателями из ТЕРРА и список месторождений.

    :param data_base_prod: строка пути к файлу или словарь с данными листов excel-файла.
    :param end_date: последняя дата прогноза.
    :param date_analysis: дата последнего факта.
    :return: словарь с показателями из ТЕРРА и список месторождений.
    """
    if isinstance(data_base_prod, (Path, str)):
        file = pd.read_excel(data_base_prod, sheet_name=None, header=1)
    else:
        file = data_base_prod
    sheets = list(file.keys())
    gtm_sheets = []
    for i in sheets:
        if i.find(GTMNames.GTM_SHEET) != -1:
            gtm_sheets.append(i)
        else:
            bd_reinj_sheet = i

    bd_data = read_bd_reinj_from_file(file[bd_reinj_sheet], end_date, date_analysis)

    def search_func(test_value: str):
        """
        Поиск уникального значения в столбце FIELD.

        :param test_value: подстрока.
        :return: индекс найденного значения.
        """
        res = np.where(bd_data[SC.FIELD].str.contains(test_value))[0]
        if len(res) != 1:
            return
        return res[0]

    def _normalize_df(df: pd.DataFrame):
        """
        Корректировка сырого датафрейма с данными по месторождениям.

        :param df: датафрейм с данными по месторождениям.
        :return: скорректированный датафрейм.
        """
        _df = df.copy().T
        _df.columns = _df.loc[SC.FIELD]
        _df = _df.drop([SC.FIELD])
        _df = to_numeric(_df, axis=0)
        _df.index = pd.to_datetime(_df.index)
        return _df

    indicators = [
        SC.OIL_PRODUCTION,
        SC.LIQUID_PRODUCTION,
        SC.GENERAL_INJECTION,
        SC.AVERAGE_OPERATING_FUND,
        SC.OPERATING_FACTOR,
        SC.GAS_PRODUCTION,
        SC.OPERATING_FUND_MONTH,
        SC.WELLS_IN_MONTH,
        SC.WELLS_OUT_MONTH,
        SC.WELLS_OUT_PPD,
        SC.WELLS_OUT_UNUSED,
        SC.WELLS_OUT_ZBS,
        SC.WELLS_OUT_TO_RETURN
    ]
    ind_values = list(map(search_func, indicators))

    ind_rows = dict(zip(indicators, ind_values))
    ind_rows = {k: v for k, v in ind_rows.items() if v is not None}
    ind_rows = {k: v for k, v in sorted(ind_rows.items(), key=lambda item: item[1])}
    indicators_dfs = {}

    for key, idx in ind_rows.items():
        next_idx = bd_data[SC.FIELD].iloc[(idx + 1):].eq(SC.TOTAL).idxmax()
        indicators_dfs[key] = _normalize_df(bd_data.iloc[slice(idx + 1, next_idx), :])

    list_of_fields = indicators_dfs[SC.OIL_PRODUCTION].columns.to_list()

    if not indicators_dfs.get(SC.OPERATING_FACTOR, pd.DataFrame()).empty:
        indicators_dfs[SC.OPERATING_FACTOR] = fill_operating_factor(
            indicators_dfs[SC.OPERATING_FACTOR]
        )
        indicators_dfs[SC.GENERAL_INJECTION] = indicators_dfs[SC.GENERAL_INJECTION].T
    else:
        indicators_dfs[SC.GENERAL_INJECTION] = \
            pd.DataFrame(indicators_dfs[SC.GENERAL_INJECTION].T.sum()).T

    if len(gtm_sheets) != 0:
        all_gtm_data = pd.DataFrame()
        for i in gtm_sheets:
            all_gtm_data = pd.concat([all_gtm_data, file[i]], ignore_index=True)

        all_dates = [x for x in bd_data.columns if isinstance(x, date)]
        gtm_data = read_gtm_from_file(all_gtm_data, all_dates)
        indicators_dfs['gtm'] = gtm_data

    return indicators_dfs, list_of_fields


def read_ois_from_file(path: Path) -> pd.DataFrame:
    """
    Чтение файла с выгрузкой из 'Справочника параметров скважин' (СПСКВ).

    :param path: путь к файлу СПСКВ.
    :return: таблица с параметрами скважин.
    """
    df = pd.read_excel(path, header=None)

    header_rows = [6, 7, 8]
    skip_rows_after_header = 2

    def correct_header(x: pd.Series):
        _x = x.str.replace('\n', ' ').str.replace(r'\s+', ' ', regex=True).str.strip()
        return ' '.join(_x).strip()

    df.columns = df.iloc[header_rows].apply(correct_header, axis=0)
    skip_rows = max(header_rows) + skip_rows_after_header + 1
    df = df.iloc[skip_rows:, :]
    df = df[
        (df[OISNames.WELL_TYPE] == SC.WELL_TYPE_OIL)
        & df[OISNames.FUND_STATE].isin([SC.FUND_STATE_WORK, SC.FUND_STATE_STOP])
    ]
    df[OISNames.STR_NAMES] = df[OISNames.STR_NAMES].astype('string')
    df = df.rename(columns={OISNames.WELL: SC.WELL})
    return df.reset_index(drop=True)


def fill_operating_factor(operating_factor: pd.DataFrame) -> pd.DataFrame:
    """
    Заполнение пустых и нулевых строк в КЭ.

    :param operating_factor: КЭ по месторождениям.
    :return: КЭ по месторождениям с отсутствием пустых и нулевых элементов.
    """
    operating_factor[operating_factor == 0.] = np.nan
    operating_factor = operating_factor.ffill()
    operating_factor[operating_factor.isna()] = Const.DEFAULT_OPERATING_FACTOR
    return operating_factor


def convert_bd_to_dict(fields: List[str], data: pd.DataFrame) -> Dict:
    """Возвращает словарь созданный из DataFrame.

    :param fields: список месторождений.
    :param data: DataFrame по БД.
    :return: словарь с информацией о данных по месторождениям.
    """
    initial_dict = data.to_dict('records')
    return {key: value for key, value in zip(fields, initial_dict)}


def convert_mer_to_dict(data: pd.DataFrame) -> List[Dict]:
    """Возвращает список созданный на основе строки DataFrame.

    :param data: строка из DataFrame по МЭР.
    :return: список словарей с построчной информацией из МЭР.
    """
    new_df = data[ColumnNames.USE_COLUMNS_FOR_MER_RU]
    new_df.columns = ColumnNames.USE_COLUMNS_FOR_MER_EN
    return new_df.to_dict('records')


def convert_terra_to_dict(data: Dict[str, pd.DataFrame]) -> List[Dict]:
    """Возвращает список созданный на основе строки DataFrame.

    :param data: строка из DataFrame по МЭР.
    :return: список словарей с построчной информацией из разбитых данных по Терре.
    """
    def create_dict_production(data_production: pd.DataFrame) -> Dict:

        production = data_production.T.to_dict('records')
        return {key: value for key, value in zip(data_production.columns, production)}

    oil_dict, liq_dict, gas_dict = [
        create_dict_production(df)
        for df in [data[SC.OIL_PRODUCTION], data[SC.LIQUID_PRODUCTION], data[SC.GAS_PRODUCTION]]
    ]

    return [{
        'WellName': key,
        'OilProductionWells': val,
        'LiquidProductionWells': liq_dict[key],
        'GasProductionWells': gas_dict[key]
    } for key, val in oil_dict.items()]


def convert_gtm(data: pd.DataFrame) -> Dict:
    """Возвращает словарь созданный из DataFrame.

    :param data: DataFrame по ГТМ.
    :return: словарь с построчными данными по ГТМ.
    """
    new = data[ColumnNames.USE_COLUMNS_FOR_GTM_RU]
    new.columns = ColumnNames.USE_COLUMNS_FOR_GTM_EN
    dict_all = new.to_dict('records')
    dict_product = data.loc[:, ~data.columns.isin(
        ColumnNames.USE_COLUMNS_FOR_GTM_RU)].to_dict('records')

    result = {}
    for index, value in enumerate(dict_all):
        value['Product'] = dict_product[index]
        field_gtm = result.setdefault(value['FieldName'], [])
        field_gtm.append(value)
    return result


def convert_other(fields: List[str], data: Dict[str, pd.DataFrame]) -> Dict:
    """Возвращает словарь словарей.

    :param fields: список месторождений.
    :param data: словарь DataFrame.
    """
    return {k: convert_bd_to_dict(fields, v.T) for k, v in data.items()}


def find_indicators(
    bd_reinj_gtm_data: Dict[str, pd.DataFrame],
    fields: List[str]
) -> Dict[str, Dict]:
    """ Поиск индикаторов

    :param bd_reinj_gtm_data: данные гтм
    :param fields: список месторождений
    :return: словарь с показателями
    """
    dict_of_indicators = {}
    for key, idx in ColumnNames.OF_INDICATORS.items():
        if idx in bd_reinj_gtm_data.keys():
            dict_of_indicators[key] = convert_bd_to_dict(fields, bd_reinj_gtm_data[idx].T)
    return dict_of_indicators


def find_input_files(
    dir_path: Path,
    data_path: Path,
 #   input_date: datetime,
  #  end_date: datetime
) -> Tuple[Dict, List]:
    """ Поиск необходимых файлов

    :param dir_path: путь к папке с МЭРами.
    :param data_path: путь к данным ТЕРРА.
    :param input_date: дата факта.
    :param end_date: конечная прогнозная дата.
    :return: считанные входные фалйы
    """
    if not isinstance(dir_path, (Path, str)) and isinstance(data_path, (Path, str)):
        raise ValueError('Input parametres are not paths')
    if not os.path.exists(dir_path):
        raise ValueError('Directory does not exist')

    files = os.listdir(dir_path)
    mer_files = {}
    terra_pack_data_files = {}
    for file_name in files:
        if file_name.find(MERNames.MER_FILE) != -1:
            mer_files[_get_field_name(file_name)] = os.path.join(
                dir_path, file_name
            )
        elif file_name.find(SC.TERRA_FILE) != -1:
            terra_pack_data_files[_get_field_name(file_name)] = os.path.join(
                dir_path, file_name
            )

    if len(mer_files.keys()) == 0 and len(terra_pack_data_files.keys()) == 0:
        raise FileNotFoundError

    #name_suborg = _get_name_suborg(data_path)
    #bd_reinj_gtm_data, fields = read_bd_reinj_gtm_file(data_path, end_date, input_date)
    mer_dict = {
        field: read_mer_from_file(Path(mer))
        for field, mer in mer_files.items()
    }
    # pack_terra = {
    #     field: read_bd_reinj_gtm_file(
    #         Path(terra_pack_data_files[normalize(field)]),
    #         end_date,
    #         input_date
    #     )[0] for field in fields
    #     if normalize(field) in terra_pack_data_files.keys()
    # }
    return mer_dict, list(mer_dict.keys())

DateFloatData = Dict[str, Dict[pd.Timestamp, float]]







