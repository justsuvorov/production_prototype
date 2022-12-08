import datetime as dt
from dateutil.relativedelta import relativedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np

import datareader as DR
#from schemas.input_pack import InputSuborg
#from utils.schemas import ClassifiedObjectsData
from BASEcalculator import BASECalculator

from Tatyana_Prod.OilProd.ArpsOilTechnique import ArpsPredictionTechnique
#from OilProd.OilAndWCTechnique import OilandWCPredictionTechnique
from Tatyana_Prod.OilProd.WC_with_integral import OilandWCPredictionTechnique
from Tatyana_Prod.LiqProd.LiqAndWCTechnique import LiqandWCPredictionTechnique
from Tatyana_Prod.LiqProd.ArpsTechnique import ArpsLiqPredictionTechnique
from Tatyana_Prod.LiqProd.ExpTechnique import ExpPredictionTechnique
from Tatyana_Prod.LiqProd.BuckleyLeverettTechnique import BLPredictionTechnique
from Tatyana_Prod.WaterCut.CoreyOizTechnique import CoreyPredictionTechnique
from Tatyana_Prod.WaterCut.CircTechnique import CircPredictionTechnique

from Domain.WellDO import WellDo

from constants import (
    DatetimeFormat,
    FluidConstans as FC,
    LiquidProductionNames,
    MERNames,
    OilProductionNames,
    StringConstants as SC,
    TFileInput,
    HOURS_IN_DAY
)



class OilPredictionMethod(Enum):
    WC = 'watercut'
    ARPS = 'arps'


class FluidPredictionMethod(Enum):
    ARPS = 'arps'
    EXP = 'exponential'
    BL = 'BuckleyLeverett'


class WCPredictionMethod(Enum):
    COREY = 'Corey'
    COMB = 'depending'



class Calculator(BASECalculator):
    """Калькулятор"""
    ##Данные по движению фонда не учитываются
    ##Закачка и ПГ пока не учитываются
    ##Нормировок на Терру нет
    #INPUT_SCHEMA = InputSuborg

    def __init__(
        self,
        date_analysis: dt.datetime,
        end_date: dt.datetime,
        name_suborg: str, #содержиться внутри well
        dict_data: Optional[Dict] = None, #заменить на Wells
        field: Optional[List] = None,
        #hierarchy: Optional[ClassifiedObjectsData] = None,
        bf_date: Optional[dt.datetime] = None,
        dir: Optional[TFileInput] = None,
        arps_coeffs: Optional[Dict] = None,
        binding_period: int = FC.DEFAULT_BINDING_PERIOD,
    ) -> None:
        """ Инициализация.

        :param date_analysis: последняя дата факта.
        :param end_date: последняя дата прогноза.
        :param name_suborg: название ДО.
        :param schema_data: входная схема.
        :param dict_data: данные не пропущенные через схему
        :param bf_date: дата формирования базового фонда.
        :param binding_period: период привязки.
        """
        super().__init__(data=None)
        self.end_date = end_date
        self.date_analysis = date_analysis
        self.start_month = dt.datetime(date_analysis.year, date_analysis.month, 1)
        self.binding_period = pd.date_range(
            start=self.start_month - relativedelta(months=binding_period - 1),
            end=self.start_month,
            freq='MS'
        )
        self.field = field[0]
        self.dir = dir


        self.mer_dict = self._prepare_mer(dict_data) #self.wells = wells
        #self.data = dict_data['bd_reinj_gtm']
        #self.pack_data = dict_data['pack_data_terra']

        #self.hierarchy = hierarchy
        # Excel файле, нужна для передачи в выходную схему
        self.name_suborg = name_suborg
        self.bf_date = bf_date


    @classmethod
    def load(
        cls,
        data_base_prod: TFileInput,
        data_mer: TFileInput,
        input_date: dt.datetime,
        end_date: dt.datetime,
        #hierarchy: Optional[ClassifiedObjectsData] = None,
        bf_date: Optional[dt.datetime] = None,
    ):
        """Возвращает дату анализа, имя ДО, входные данные в виде входной схемы, словарь со входными
            данными.
        :param data_base_prod: путь к файлу БД+Закачка+ГТМ или сырые считанные данные
                в виде словаря листов excel-файла.
        :param data_mer: путь к папке с МЭРами и разбитыми данными из Терры или
                считанные сырые данные в виде словаря.
        :param input_date: дата анализа.
        :param end_date: последняя дата прогноза.
        :param bf_date: дата формирования базового фонда.
        """
        print('Start preparing data')
        """
        убрать
        """
        bd_reinj_gtm_data, mer_dict, terra_pack_data_dict, name_suborg, fields = \
            cls._prepare_data(data_base_prod, data_mer, input_date, end_date)
        print('Data was prepared')

        dict_data = {
            'bd_reinj_gtm': {},
            'mer': mer_dict,
            'pack_data_terra': {},
        }

        return cls(
            input_date,
            end_date,
            name_suborg,
            dict_data, #убрать
            fields,
            #hierarchy,
            bf_date,
            data_base_prod
        )



    @staticmethod
    def _prepare_data(
        data_path: TFileInput,
        dir_path: TFileInput,
        input_date: dt.datetime,
        end_date: dt.datetime,
    ):
        """Возвращает обработанные данные базовой добычи Мэров и Теровских файлов.

        :param data_path: путь к файлу БД+Закачка+ГТМ или сырые считанные данные
        в виде словаря листов excel-файла.
        :param dir_path: путь к папке с МЭРами и разбитыми данными из Терры или
        считанные сырые данные в виде словаря.
        :param input_date: дата анализа.
        :param end_date: последняя дата прогноза.
        """

        """
        Убрать
        """
        if isinstance(dir_path, (Path, str)) and isinstance(data_path, (Path, str)):
            mer_dict, fields = DR.find_input_files(
                dir_path,
                data_path,
                input_date,
                end_date
            )
        elif isinstance(dir_path, Dict) and isinstance(data_path, Dict):
            name_suborg = list(data_path.keys())[0]
            bd_gtm, fields = [val for key, val in data_path[name_suborg].items()]
            bd_reinj_gtm_data = DR.read_bd_reinj_gtm_file(bd_gtm, end_date, input_date)[0]
            mer_dict = {
                key: DR.read_mer_from_file(val) for key, val in dir_path[SC.MER_DATA][name_suborg].items()
            }
            if len(dir_path[SC.TERRA_DATA]) > 0:
                pack_terra = {
                    key: DR.read_bd_reinj_gtm_file(val, end_date, input_date)[0]
                    for key, val in dir_path[SC.TERRA_DATA][name_suborg].items()
                }
            else:
                pack_terra = {}
        else:
            raise ValueError('Нет корректных данных для расчета')
        return {}, mer_dict, {}, '', fields

    """Вынести в модуль creator"""
    def _prepare_mer(self, mer):
        mer = mer['mer'].get(self.field)
        #mer = mer.loc[['2186', '4143', '4135', '2086', '9315', '4130', '4097']].sort_values(by=[MERNames.WELL, MERNames.DATE])
        mer = mer.loc[['4143', '4135']].sort_values(by=[MERNames.WELL, MERNames.DATE])

        mer = mer.loc[(mer[MERNames.DATE] <= self.date_analysis) & (mer[MERNames.OIL_PRODUCTION] > 0)]
        wells = mer.loc[mer[SC.DATE].isin(self.binding_period), :].index.unique()
        mer = mer.loc[mer[MERNames.WELL].isin(wells), :]
        print(mer)
        return mer



    """
    заменить data на wells, которые инкапсулированы. 
    mer_data = self.wells.data()
    Это модуль подготовки данных. в отдельный модуль (Adapter)
    """
    def calc_use_coef(self, data: pd.DataFrame, bind_period: int) -> pd.DataFrame:
        """ Расчет среднего коэффициента эксплуатации по скважинам

        :param data: данные МЭР.
        :param bind_period: период привязки.
        :return : коэффициенты эксплуатации
        """
        bind_period = pd.date_range(
            start=self.start_month - relativedelta(months=bind_period - 1),
            end=self.start_month,
            freq='MS'
        )
        mer_data = data.rename(columns={MERNames.WELL: SC.WELL})
        mer_data = mer_data.astype({SC.WELL: 'str'})
        mer_data.set_index([SC.WELL], inplace=True)
        mer_data = mer_data.loc[
                (mer_data[MERNames.OPERATING_TIME_HPM]) > 0,
                [SC.DATE, MERNames.OPERATING_TIME_HPM]
            ]
        #пока что расчёт для скважин, работавших в период привязки
        mer_data = mer_data.loc[mer_data[SC.DATE].isin(bind_period), :]
        ####
        max_time = pd.DatetimeIndex(mer_data[SC.DATE].values).days_in_month * HOURS_IN_DAY
        mer_data[MERNames.OPERATING_TIME_HPM] /= max_time
        mer_data = mer_data.drop(SC.DATE, axis=1).groupby(mer_data.index).mean()
        mer_data = mer_data.rename(columns={MERNames.OPERATING_TIME_HPM: 'КЭ'})
        return mer_data


    def run(self, log_time=True, **kwargs):
        """Запуск калькулятора."""
        self.log('Расчет запущен')
        self.result = self._calculate(**kwargs)
        self.log('Данные рассчитаны')
        return self.result

    def predict_new_wells(self, new_wells_list: List, IRR: pd.DataFrame, const: pd.DataFrame):
        """Схема расчёта для скважин, которые проработали меньше 4 месяцев"""
        all_oil = pd.DataFrame(columns=self.dateline)
        all_liq = pd.DataFrame(columns=self.dateline)
        all_wc = pd.DataFrame(columns=self.dateline)
        niz_oiz = pd.DataFrame(columns=['NIZ', 'OIZ start', 'OIZ end'])
        # временно, пока строим графики, выводим еще два датафрейма
        const = pd.DataFrame(columns=['CoreyO', 'CoreyW', 'Mu', 'b1', 'b2', 'd1', 'tau', 'qst', 'ke'])
        time = pd.DataFrame(columns=self.dateline)
        wells_id = []


        """
        Перенести в модуль WellsCreator
        """
        for id in new_wells_list:
            print(mer_well)
            mer_well = self.mer_dict.loc[self.mer_dict.index == id]
            well = WellDo(id, mer_well, self.bf_date)
            well.get_state(self.start_month)
            wells_id.append(id)

        all_oil.insert(0, 'well', wells_id)
        all_liq.insert(0, "well", wells_id)
        all_wc.insert(0, "well", wells_id)
        niz_oiz.insert(0, "well", wells_id)
        # yбрать
        const.insert(0, "well", wells_id)
        time.insert(0, 'well', wells_id)

        all_oil = all_oil.set_index('well')
        all_liq = all_liq.set_index('well')
        all_wc = all_wc.set_index('well')
        niz_oiz = niz_oiz.set_index('well')
        # убрать
        const = const.set_index('well')
        time = time.set_index('well')

        return [all_oil, all_liq, all_wc, time], niz_oiz, const


    def scheme_high(self, wells_high_wc: pd.DataFrame, need_oil: bool):
        """Схема прогнозного расчета для скважин с высокой обводнённостью."""

        self.watercut_pt = CircPredictionTechnique(
            prod_names=LiquidProductionNames,
            binding_period=self.binding_period,
            constraints=self.const
        )

        for id in wells_high_wc:
            mer_well = self.mer_dict.loc[self.mer_dict.index==id]
            well = WellDo(id, mer_well, self.bf_date)
            well.get_state(self.start_month)
            wc_high = self.watercut_pt.calc_wc(well, self.start_month)
            if need_oil:
                m_liq = self.liquid_pt.calc_liq(well, self.start_month)
                m_oil = self.oil_pt.calc_oil(well, self.start_month, self.end_date, wc_high, m_liq,  self.use_coef)
            else:
                m_oil = None
                m_liq = None
        return m_oil, m_liq, wc_high


    def scheme_low(self, wells_normal: pd.DataFrame, need_oil: bool):
        """Схема прогнозного расчета для скважин с низкой обводнённостью."""

        self.watercut_pt = CoreyPredictionTechnique(
            prod_names=LiquidProductionNames,
            binding_period=self.binding_period,
            constraints=self.const
        )

        for id in wells_normal:
            mer_well = self.mer_dict.loc[self.mer_dict.index==id]
            well = WellDo(id, mer_well, self.bf_date)
            well.get_state(self.start_month)
            wc_low = self.watercut_pt.calc_wc(well, self.start_month)
            if need_oil:
                m_liq = self.liquid_pt.calc_liq(well, self.start_month)
                m_oil = self.oil_pt.calc_oil(well, self.start_month, self.end_date, wc_low, m_liq,  self.use_coef)
            else:
                m_oil = None
                m_liq = None
        return m_oil, m_liq, wc_low


    def scheme_normal(self, wells: List, need_oil: bool
                      ) -> Tuple[List[pd.DataFrame], List, pd.DataFrame,  pd.DataFrame]:
        """Схема прогнозного расчета для скважин, если уровень обводнённости не учитывается."""
        all_oil = pd.DataFrame(columns=self.dateline)
        all_liq = pd.DataFrame(columns=self.dateline)
        all_wc = pd.DataFrame(columns=self.dateline)
        niz_oiz = pd.DataFrame(columns=['NIZ', 'OIZ start', 'OIZ end'])
        #временно, пока строим графики, выводим еще два датафрейма
        const = pd.DataFrame(columns=['CoreyO', 'CoreyW', 'Mu', 'b1', 'b2', 'd1', 'tau', 'qst', 'ke'])
        time = pd.DataFrame()
        new_wells = []
        wells_id = []

        """Переработать"""
        for id in wells:
            mer_well = self.mer_dict.loc[self.mer_dict.index == id]
            #доступ к merwell через well.data()

            well = WellDo(id, mer_well, self.bf_date)
            well.get_state(self.start_month) #работа с well(wellInfo(status))
            wc = self.watercut_pt.calc_wc(well, self.start_month)

            if need_oil:
                model = self.liquid_pt.main_calc(well, self.start_month)
                m_oil, well = self.oil_pt.calc_oil(well, self.start_month, self.end_date, wc, model)
            else:
                model = self.oil_pt.calc_oil(well, self.start_month)
                m_liq, well = self.liquid_pt.calc_liq(well, self.start_month, self.end_date, wc, model)

            if model.new_wells is None:
                wells_id.append(id)
                print('!!!!!!!!   ' + str(id) + '     is done')
                niz_oiz = niz_oiz.append(
                    pd.DataFrame(data={'NIZ': well.NIZ, 'OIZ start': well.OIZ, 'OIZ end': well.OIZ_end},
                                 index=[id]), ignore_index=True)
                all_oil = all_oil.append(well.prediction_oil, ignore_index=True, sort=True).fillna(0)
                all_liq = all_liq.append(well.prediction_liq, ignore_index=True, sort=True).fillna(0)
                all_wc = all_wc.append(well.prediction_wc, ignore_index=True, sort=True).fillna(0)
                const = const.append(
                    pd.DataFrame(data={'CoreyO': wc.corey_oil, 'CoreyW': wc.corey_water, 'Mu': wc.mef,
                                       'b1': model.b1, 'b2': model.b2, 'd1': model.D1, 'tau': model.t,
                                       'qst': model.start_q, 'ke': well.ke}, index=[id]), ignore_index=True)
                time = time.append(well.time, ignore_index=True, sort=True).fillna(0)
            else:
                new_wells.append(id)


        all_oil.insert(0, 'well', wells_id)
        all_liq.insert(0, "well", wells_id)
        all_wc.insert(0, "well", wells_id)
        niz_oiz.insert(0, "well", wells_id)
        #yбрать
        const.insert(0, "well", wells_id)
        time.insert(0, "well", wells_id)

        all_oil = all_oil.set_index('well')
        all_liq = all_liq.set_index('well')
        all_wc = all_wc.set_index('well')
        niz_oiz = niz_oiz.set_index('well')
        #убрать
        const = const.set_index('well')
        time = time.set_index('well')

        return [all_oil, all_liq, all_wc, time], [wells_id, new_wells], niz_oiz, const



    def _calculate(
        self,
        oil_method: Enum,
        fluid_method: Enum,
        watercut_method: Enum,
        start_date: dt.datetime,
        cut_date: dt.datetime,
        account_condensate: bool = False,
        mean_use_coef: bool = False,
        binding_to_mean: bool = True,
    ) -> List[pd.DataFrame]:
        """Возвращает список, содержащий 5 DataFrame: добыча нефти, добыча жидкости

        :param oil_method: метод прогноза добычи нефти.
        :param fluid_method: метод прогноза добычи жидкости.
        :param watercut_method: метод прогноза ХВ.
        :param cumulative_scale: нормировка на накопленную.
        :param const: массив ГУ для констант, находимых в процессе моделированя
                    Кори(нефть, жидкость), Модуль вязкости (снизу, сверху), коэфф. Арпса (снизу, сверху для обоих).
        :param wc_shelf: DataFrame со значением обводнённости скважин на последнюю дату факта.
        :param binding_to_mean: True привязка к среднему, иначе к последнему месяцу факта
        """

        self.oil_method = oil_method
        self.fluid_method = fluid_method
        self.watercut_method = watercut_method
        self.scale_predicted_prod = False
        self.start_date = start_date
        self.cut_date = cut_date
        self.binding_to_mean = binding_to_mean
        self.mean_use_coef = mean_use_coef
        self.const = np.zeros(8)
        self.wc_shelf = None

        if self.wc_shelf is not None:
            #если для скважин с различной обводнённостью будут заданы начальные обводнённости
            #будет происходить автоматический выбор схемы прогноза
            #скважины делятся по степени обводнённости (>0.65) и для них выбираются различные модели ХВ
            wells_high_wc = self.wc_shelf.loc[[self.wc_shelf['WC']>0.65]]
            wells_normal = self.wc_shelf.drop(wells_high_wc.index)

        self.use_coef = self.calc_use_coef(self.mer_dict, 3)
        #тут будет подготовка ГТМ данных для испльзования в модуле ХВ и\или жидкости
        print(self.mer_dict)
        well_list = self.mer_dict.index.unique().tolist()
        well_list.sort()
        time_forecast = 12*(self.end_date.year - self.date_analysis.year) + (self.end_date.month - self.date_analysis.month)
        list = np.arange(1, time_forecast+1, 1).tolist()
        self.dateline = [self.date_analysis + relativedelta(months = i) for i in list]


        #выбор прогнозных моделей
        if self.oil_method == OilPredictionMethod.ARPS:
            self.oil_pt = ArpsPredictionTechnique(
                #prod_names=LiquidProductionNames,
                binding=binding_to_mean,
                binding_period=self.binding_period,
                constraints=self.const,
                search_gtm=False,
                polka=False,
            )
            self.liquid_pt = LiqandWCPredictionTechnique(
                #prod_names=LiquidProductionNames,
                use_koeff=self.use_coef,
                #binding_period=3,
            )
        else:
            self.oil_pt = OilandWCPredictionTechnique(
                prod_names=OilProductionNames,
                use_koeff=self.use_coef,
                binding_period=3,
                ret_only_base_prod=True,
                account_condensate=account_condensate,
            )

            if self.fluid_method == FluidPredictionMethod.ARPS:
                self.liquid_pt = ArpsLiqPredictionTechnique(
                    prod_names=LiquidProductionNames,
                    binding=binding_to_mean,
                    binding_period=self.binding_period,
                    constraints=self.const,
                    search_gtm=False,
                    polka=False,
                )
            elif self.fluid_method == FluidPredictionMethod.BL:
                self.liquid_pt = BLPredictionTechnique(
                    prod_names=LiquidProductionNames,
                    binding=binding_to_mean,
                    binding_period=self.binding_period,
                    constraints=self.const,
                )
            else:
                self.liquid_pt = ExpPredictionTechnique(
                    prod_names=LiquidProductionNames,
                    binding=binding_to_mean,
                    binding_period=self.binding_period,
                    constraints=self.const,
                )

        if self.wc_shelf is None:
            self.watercut_pt = CoreyPredictionTechnique(
                prod_names=LiquidProductionNames,
                binding=binding_to_mean,
                binding_period=self.binding_period,
                constraints=self.const,
            )



        if self.oil_method == OilPredictionMethod.ARPS:
            need_oil = False
        #     #oil, liq можно считать независимо друг от друга
        #     for id in well_list:
        #         mer_well = self.mer_dict.loc[self.mer_dict.index==id]
        #         well = WellDo(id, mer_well, self.bf_date)
        #         well.get_state(self.start_month)
        #
        #         #m_liq = self.liquid_pt.calc_liq(well, self.start_month)
        #         m_oil = self.oil_pt.calc_oil(well, self.start_month)
        #     if self.wc_shelf is not None:
        #         _, _, wc_high = self.scheme_high(wells_high_wc, need_oil=False)
        #         _, _, wc_low = self.scheme_low(wells_normal, need_oil=False)
        #     else:
        #         all_data, new_wells_list, irr, const = self.scheme_normal(well_list, need_oil=False)
        #
        else:
            need_oil = True
        if self.wc_shelf is not None:
            # oil, liq связаны с моделью обводнённости, считаем вместе
            all_data, wells_lists, irr, const = self.scheme_high(wells_high_wc, need_oil)
            all_data_, wells_lists_, irr_, const_ = self.scheme_low(wells_normal, need_oil)
        else:
            all_data, wells_lists, irr, const = self.scheme_normal(well_list, need_oil)

        new_wells_list = wells_lists[1]
        if new_wells_list:
            self.predict_new_wells(new_wells_list, irr, const)
        data_args = all_data + [irr, const] + [wells_lists[0]]

        self.cut_result_and_save(*data_args)

        return data_args




    def cut_result_and_save(self, *prods, output: str = None, include_index: bool = True):
        """Обрезает результат с определенной даты.

        :param start_date: дата с которой нужно обрезать результат
        :param prods: добыча по разным параметрам
        :return: обрезанные с определенной даты результаты
        """
        prod_oil = prods[0]
        prod_liq = prods[1]
        wc_ch = prods[2]
        irr = prods[4]
        const = prods[5]
        start_date = self.cut_date

        prod_oil = prod_oil[prod_oil.columns[prod_oil.columns >= start_date]]
        prod_liq = prod_liq[prod_liq.columns[prod_liq.columns >= start_date]]
        wc_ch = wc_ch[wc_ch.columns[wc_ch.columns >= start_date]]


        TEMP_DIR = self.dir
        if not output:
            filename = f'{SC.DEFAULT_OUTPUT_PREFIX}_{self.name_suborg}{SC.EXTENSION}'
            output = str(TEMP_DIR / filename)

        writer = pd.ExcelWriter(output, datetime_format=DatetimeFormat.OutputDate)

        prod_liq.to_excel(writer, sheet_name='Дебит жидкости, т.день', index=include_index)
        prod_oil.to_excel(writer, sheet_name="Дебит нефти, т.день", index=include_index)
        irr.to_excel(writer, sheet_name='Обводнённость', index=include_index)
        wc_ch.to_excel(writer, sheet_name='Обводнённость', startcol=4, index=include_index)
        # нужны для визуализации, потом можно убрать
        const.to_excel(writer, sheet_name='Константы', index=include_index)

        writer.save()
        print({'Данные сохранены'})





