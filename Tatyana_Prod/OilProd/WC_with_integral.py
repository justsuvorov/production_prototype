from datetime import datetime
from typing import Type, Optional, Union
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import calendar


from constants import (
    AVG_DAYS_IN_MONTH,
    HOURS_IN_DAY,
    MERNames,
    ProductionNames,
)
from constants import StringConstants as SC
from constants import ConstantsForCalc as Const
from Tatyana_Prod.arps_function import CombinedArps
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
        #use_koeff.loc[use_koeff['КЭ']<=0.90] = 0.95
        self.use_koeff = use_koeff



    def calc_oil(self, well: WellDo,
                  on_date: datetime, off_date: datetime,
                  wc_model: Optional[CoreyModel] = None,
                  liq_model: Optional[LiqModel] = None,
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

        model = OilModel(well, on_date, off_date, sum_condensate=False)
        time_forecast = 12*(off_date.year - on_date.year) + (off_date.month - on_date.month)
        list = np.arange(1, time_forecast + 1, 1).tolist()
        self.dateline = [on_date + relativedelta(months=i) for i in list]

        Qn_t = [0]
        Qn = []
        Wc_mod = []
        Qliq = []

        if liq_model.new_wells is not None:
            # если скважина работала меньше 4 месяцев, она будет рассчитана как среднее по месторождению
            model.new_wells = well.wellID
            well.OIZ = wc_model.OIZ
            well.NIZ = wc_model.NIZ
            return model, well

        if liq_model.double_arps == True:
            #Qliq = np.zeros(time_forecast)
            now_RF = wc_model.RF_last_fact
            num_m = well.mer[MERNames.OIL_PRODUCTION].size + 1

            arps_coeffs = np.array([liq_model.b1, liq_model.b2, liq_model.D1, liq_model.t])
            Qliq = self.calc_liq_by_integral(well, on_date, arps_coeffs) * liq_model.start_q/self.use_koeff.loc[well.wellID, 'КЭ']
            Qliq = Qliq.loc[:, Qliq.columns > on_date].values.tolist()[0]
            for i in range(time_forecast):
                now_RF = now_RF + Qn_t[-1] / wc_model.NIZ / 1000
                if now_RF >= 1: now_RF = 0.99999999999
                Wc_mod.append(self.calc_wc(wc_model.corey_oil, wc_model.corey_water, wc_model.mef, now_RF))
                num_m += 1
                Qn.append(Qliq[i] * (1 - Wc_mod[-1]))
                days_in_month = calendar.monthrange(on_date.year, on_date.month)[1]
                Qn_t.append(Qn[i] * days_in_month)

        else:
            now_RF = wc_model.RF_last_fact
            num_m = well.mer[MERNames.OIL_PRODUCTION].size + 1
            for i in range(time_forecast):
                now_RF = now_RF + Qn_t[-1] / wc_model.NIZ / 1000
                if now_RF >= 1: now_RF = 0.99999999999
                Wc_mod.append(self.calc_wc(wc_model.corey_oil, wc_model.corey_water, wc_model.mef, now_RF))
                Qliq.append(self.calc_liq(liq_model.start_q, liq_model.k1, liq_model.k2, num_m))
                num_m += 1
                Qn.append(Qliq[-1] * (1 - Wc_mod[-1]))
                days_in_month = calendar.monthrange(on_date.year, on_date.month)[1]
                Qn_t.append(Qn[-1] * days_in_month)

        Q_nak_pred = np.cumsum(Qn_t) / 1000
        well.prediction_oil = pd.Series(Qn, index=self.dateline)
        well.prediction_liq = pd.Series(Qliq, index=self.dateline)
        well.prediction_wc = pd.Series(Wc_mod, index=self.dateline)
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
        fact_oil = mer[MERNames.OIL_PRODUCTION]
        fact_liq = mer[MERNames.LIQUID_PRODUCTION]
        fact_time = mer[MERNames.OPERATING_TIME_HPM].div(24)

        #пока считаем дебит, надо делить
        fact_oil = fact_oil.div(fact_time)
        fact_liq = fact_liq.div(fact_time)
        wc_fact = fact_oil.div(fact_liq).add(-1) * (-1)

        well.prediction_oil = pd.concat([fact_oil, well.prediction_oil])
        well.prediction_liq = pd.concat([fact_liq, well.prediction_liq])
        well.prediction_wc = pd.concat([wc_fact, well.prediction_wc])
        #well.time =

        return well


    def calc_liq_by_integral(self, well, on_date, arps_coeffs):
        first_binding_date = on_date + relativedelta(months=-3)
        use_coef = self.use_koeff.loc[well.wellID, 'КЭ']
        ct = self.get_c_time(mer=well.mer, use_k=use_coef, start_date=first_binding_date, ondate=on_date)
        predict_ct = pd.DataFrame({k: use_coef for k in self.dateline}, index=[well.wellID]).cumsum(axis=1)
        predict_ct = predict_ct.add(ct.loc[predict_ct.index, on_date], axis=0)
        ct = pd.concat([ct, predict_ct], axis=1).fillna(0.)

        well.get_ke(self.use_koeff)
        arps_values = ct.apply(lambda x: self.arps_integral(x, arps_coeffs=arps_coeffs), axis=1)

        return arps_values


    def get_c_time(self,
        mer: pd.DataFrame,
        use_k,
        start_date: datetime = None,
        ondate: datetime = None,
    ) -> pd.DataFrame:
        """Расчет фактического накопленного времени.

        :param df: Разделенная добыча нефти
        :param mer: Данные МЭР
        :param start_date: дата начала прогнозного периода
        :return: Накопленное время на фактический период
        """
        ct = mer.groupby(mer.index).aggregate(
            CumulativeTime=pd.NamedAgg(column=MERNames.OPERATING_TIME_HPM,
                                       aggfunc='cumsum')) / (HOURS_IN_DAY * AVG_DAYS_IN_MONTH)
        ct.insert(0, SC.DATE, mer[SC.DATE])
        last_fact = ct[SC.DATE][-1]
        if last_fact < (self.dateline[0] + relativedelta(months=-1)):
            num = self.calc_months(last_fact, ondate)
            patch_time = pd.Series([last_fact + relativedelta(months=i+1) for i in range(num)])
            ct = ct.append(pd.DataFrame(data={SC.DATE: patch_time, 'CumulativeTime': np.array([ct['CumulativeTime'][-1]+use_k*(i+1) for i in range(num)])}), ignore_index=True, sort=True).fillna(0)
            ct = ct.set_index(np.array([mer.index[0] for i in ct.index]))
        ct = ct.pivot_table('CumulativeTime', index=ct.index, columns=SC.DATE)
        #ct.index = pd.MultiIndex.from_tuples(ct.index, names=[SC.WELL])

        ct = ct[ct.columns[ct.columns >= start_date - relativedelta(months=1)]]

        return ct.fillna(method='ffill', axis=1).fillna(0.)



    def calc_months(self, start_date: Union[datetime, pd.Timestamp], end_date: Union[datetime, pd.Timestamp]):
        return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)


    def arps_integral(self, grid, arps_coeffs):
        """Расчет интегралов на сетке от комбинированной функции Арпса для
        заданного пласта.

        :param grid: сетка для расчета интегралов.
        :param arps_coeffs: коэффициенты для функции Арпса м.
        :return: рассчитанные интегралы на отрезках.
        """
        def _calc_integral(upper):
            return CombinedArps.calc_integral(
                lower=0,
                upper=upper,
                b1=arps_coeffs[0],
                D1=arps_coeffs[2],
                b2=arps_coeffs[1],
                tau=arps_coeffs[3]
            )

        values = grid.apply(_calc_integral).to_numpy()
        n = len(values) - 1  # отрезков интегрирования на единицу меньше, чем точек

        return pd.Series(data=values[-n:] - values[:n], index=grid.index[-n:])


