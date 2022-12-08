from datetime import datetime
from typing import Type, Optional
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
from constants import (
    MERNames,
    ProductionNames
)
import calendar

from constants import ConstantsForCalc as Const
from Tatyana_Prod.Domain.WellDO import WellDo
from Tatyana_Prod.Domain.OilModelDO import OilModel
from Tatyana_Prod.Domain.CoreyModelDO import CoreyModel
from Tatyana_Prod.Domain.LiqModelDO import LiqModel


TProductionNames = Type[ProductionNames]

GTM_CORRECTED = 'gtm_corrected'
BASE_PRODUCTION = 'base_production'


class OilandWCPredictionTechnique():
    '''Класс содержит логику построения прогнозных кривых добычи нефти
       по модели характеристик вытеснения и модели добычи жидкости


    :param binding_period: период привязки
    :param substract_gtm: вычитать ГТМ при прогнозировании.
    :param ret_only_base_prod: при установке в `True` возвращается только БД. Иначе - БД + ГТМ.
    '''

    def __init__(self,
                 prod_names: TProductionNames,
                 use_koeff: pd.DataFrame,
                 binding_period: int = 3,
                 ret_only_base_prod: bool = True,
                 account_condensate: bool = False,
                 ):
        self.prod_names = prod_names
        self.default_operating_factor = Const.DEFAULT_OPERATING_FACTOR
        self.fact_production_column = self.prod_names.StandardCode
        self.oil_condensate = pd.DataFrame()
        self.use_koeff = use_koeff



    def calc_oil(self, well: WellDo,
                  on_date: datetime, off_date: datetime,
                  wc_model: Optional[CoreyModel] = None,
                  liq_model: Optional[LiqModel] = None,
                  use_coef: Optional[pd.DataFrame] = None,
                  bf_date: Optional[datetime] = None,
                  ) -> OilModel:
        """Расчет помесячной добычи для каждой скважины WellDO.

            :param well: экземпляр класса WellDO.
            :param on_date: конечная дата фактической добычи.
            :param off_date: конечная дата прогноза
            :param use_coef: предрасчитанный коэффициент эксплуатации.
            :param bf_date: дата формирования базового фонда.
            :param wc_model: оптимизированная модель ХВ.
            :param liq_model: оптимизированная модель добычи жидкости.
            :return: экземпляр класса OilModel, описывающий прогнозную модель.
                     экземпляр класса WellDo с заполненными прогнозными данными
            """

        model = OilModel(well, on_date, off_date, use_coef, sum_condensate=False)
        time_forecast = 12*(off_date.year - on_date.year) + (off_date.month - on_date.month)

        Qn_t = [0]
        Qn = []
        Wc_mod = []
        Qliq = []

        if liq_model.new_wells is not None:
            #если скважина работала меньше 4 месяцев, она будет рассчитана как среднее по месторождению
            model.new_wells = well.wellID
            well.OIZ = wc_model.OIZ
            well.NIZ = wc_model.NIZ
            return model, well


        now_RF = wc_model.RF_last_fact
        num_m = well.mer[MERNames.OIL_PRODUCTION].size + 1
        for i in range(time_forecast):
            now_RF = now_RF + Qn_t[-1] / wc_model.NIZ / 1000
            if now_RF >= 1: now_RF = 0.99999999999
            Wc_mod.append(self.calc_wc(wc_model.corey_oil, wc_model.corey_water, wc_model.mef, now_RF))
            Qliq.append(self.calc_liq(liq_model.start_q_liq, liq_model.k1, liq_model.k2, num_m))
            num_m += 1
            Qn.append(Qliq[-1] * (1 - Wc_mod[-1]))
            days_in_month = calendar.monthrange(on_date.year, on_date.month)[1]
            Qn_t.append(Qn[-1] * days_in_month)
            #on_date += timedelta(days=days_in_month)
        Q_nak_pred = np.cumsum(Qn_t)/1000

        list = np.arange(1, time_forecast + 1, 1).tolist()
        dateline = [on_date + relativedelta(months=i) for i in list]
        well.prediction_oil = pd.Series(Qn, index=dateline)
        well.prediction_liq = pd.Series(Qliq, index=dateline)
        well.prediction_wc = pd.Series(Wc_mod, index=dateline)
        well.OIZ = wc_model.OIZ
        well.NIZ = wc_model.NIZ
        well.OIZ_end = well.OIZ - Q_nak_pred[-1]

        well = self.get_fact(well, on_date)
        return model, well


    def calc_wc(self, Co, Cw, mef, now_RF):
        return mef * now_RF ** Cw / ((1 - now_RF) ** Co + mef * now_RF ** Cw)

    def calc_liq(self, Qst, k1, k2, num_m):
        return Qst * (1 + k1 * k2 * (num_m - 1)) ** (-1 / k2)

    def get_fact(self, well: WellDo, on_date: datetime):
        mer = well.mer.loc[:, [MERNames.OIL_PRODUCTION, MERNames.LIQUID_PRODUCTION, MERNames.OPERATING_TIME_HPM, MERNames.DATE]]
        mer = mer.loc[(mer[MERNames.DATE] <= on_date) & (mer[MERNames.OIL_PRODUCTION] > 0)].set_index(MERNames.DATE)
        fact_oil =  mer[MERNames.OIL_PRODUCTION]
        fact_liq =  mer[MERNames.LIQUID_PRODUCTION]
        fact_time = mer[MERNames.OPERATING_TIME_HPM].div(24)

        #пока считаем дебит, надо делить
        fact_oil = fact_oil.div(fact_time)
        fact_liq = fact_liq.div(fact_time)
        wc_fact = fact_oil.div(fact_liq).add(-1) * (-1)

        well.prediction_oil = pd.concat([fact_oil, well.prediction_oil])
        well.prediction_liq = pd.concat([fact_liq, well.prediction_liq])
        well.prediction_wc = pd.concat([wc_fact, well.prediction_wc])

        return well

    #def calc_liq_by_integral(self, ):



    #def get_c_time(self):




