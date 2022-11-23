from datetime import datetime
from typing import Type, Optional
import numpy as np
import pandas as pd
import math
from scipy.optimize import minimize, Bounds, NonlinearConstraint, fsolve
from constants import (
    MERNames,
    MetricSIPrefix,
    ProductionNames,
    StringConstants,
)

from NIZ.FindingConstraintsTechnique import OIZ

from Domain.WellDO import WellDo
from Domain.CoreyModelDO import CoreyModel

TProductionNames = Type[ProductionNames]


class CoreyPredictionTechnique():
    '''Класс содержит логику построения модели ХВ по Кори.
        Принимает на вход:
            :param const: ГУ для аргументов функции Кори
            :param binding_period: количество периодов привязки для определения начального дебита.
        Возвращает:
            экземпляр CoreyModel с оптимизированной функцией Кори
    '''

    def __init__(
            self,
            prod_names: TProductionNames,
            binding: bool,
            binding_period: int = 3,
            constraints: Optional[np.ndarray]=None,
    ):
        self.prod_names = prod_names
        self.fact_production_column = self.prod_names.StandardCode
        self.bind_to_mean = binding
        self.binding_period = binding_period
        self.const = constraints



    def calc_wc(self, well: WellDo,
            on_date: datetime,
            ) -> CoreyModel:

        ''' :param well: объект с информацией по скважине за фактический период
            :param on_date: конечная дата фактической добычи.
            :return: экземпляр класса CoreyModel, описывающий прогнозную модель добычи жидкости.'''
        mer = well.mer.loc[
                (well.mer[MERNames.OIL_PRODUCTION]) > 0]
        oiz_model = OIZ(mer).calculate_oiz()
        model = CoreyModel(well, self.const, oiz_model)
        model.check_const()
        self.const[:4] = np.array([model.corey_oil_left, model.corey_water_left,\
                                   model.mef_left, model.mef_right])

        Wc_last = 1 - mer[MERNames.OIL_PRODUCTION][-1] / mer[MERNames.LIQUID_PRODUCTION][-1]

        if Wc_last == 1:
            RF = Wc_last/(1-Wc_last)
            if oiz_model['ОИЗ Left'] is not None:
                oiz = oiz_model['ОИЗ Right'] - oiz_model['ОИЗ Left']
            else:
                oiz = oiz_model['ОИЗ Right']
        else:
            dob_neft = mer[MERNames.OIL_PRODUCTION].to_numpy()
            dob_zhid = mer[MERNames.LIQUID_PRODUCTION].to_numpy()
            model = self.Calc_CD(model, oiz_model, self.const, dob_neft, dob_zhid)
        return model




    def Calc_CD(self, cormodel:CoreyModel,
                oiz_w: pd.DataFrame, conf: np.ndarray,
                dob_neft: np.ndarray, dob_zhid: np.ndarray):
        """
        Функция для аппроксимации характеристики вытеснения
        :param cormodel: оптимизируемая модель ХВ
        :param oiz_w: начальная модель ОИЗ
        :param conf: ограничения на аппроксимацию
        :return: output - массив с коэффициентами аппроксимации
        [corey_oil; corey_water; mef; metka_text,tek_RF, oiz_w]
         0             1          2        3         4     5
        """

        """ Проверка точек обводненности"""
        Qnef_nak = np.sum(dob_neft) / 1000
        Wc_fact = (dob_zhid - dob_neft) / dob_zhid
        Wc_fact[(Wc_fact == -np.inf) | (Wc_fact == np.inf)] = 0
        cormodel.q_nak = Qnef_nak

        metka = len(Wc_fact[np.where(Wc_fact < Wc_fact[-1])]) > len(Wc_fact[np.where(Wc_fact > Wc_fact[-1])])
        corey_oil = None
        if metka:
            New_Wc_fact = Wc_fact
            New_dob_neft = dob_neft
            New_dob_zhid = dob_zhid
        else:
            New_Wc_fact = Wc_fact[np.where(Wc_fact <= Wc_fact[-1])[0]]
            New_dob_neft = dob_neft[np.where(Wc_fact <= Wc_fact[-1])[0]]
            New_dob_zhid = dob_zhid[np.where(Wc_fact <= Wc_fact[-1])[0]]

        # Оптимизация функции
        NIZ = cormodel.OIZ + Qnef_nak
        NIZ_L = cormodel.oiz_left + Qnef_nak
        NIZ_R = cormodel.oiz_right + Qnef_nak
        d_set = [cormodel.corey_oil, cormodel.corey_water, cormodel.mef, NIZ]
        CD = Characteristic_of_Desaturation(New_dob_neft, New_dob_zhid, cormodel.ID, metka,
                                            New_Wc_fact, Qnef_nak, self.bind_to_mean)
        bnds = Bounds([cormodel.corey_oil_left, cormodel.corey_water_left, cormodel.mef_left, NIZ_L],
                    [cormodel.corey_oil_right, cormodel.corey_water_right, cormodel.mef_right, NIZ_R])

        try:
            non_linear_con = NonlinearConstraint(CD.Conditions_CD, [-0.00001], [0.00001])
            res = minimize(CD.Solver, d_set, method='trust-constr', bounds=bnds, constraints=non_linear_con)
            d_set = res.x
            cormodel.corey_oil = list(res.x)[0]
            cormodel.corey_water = list(res.x)[1]
            cormodel.mef = list(res.x)[2]
            cormodel.OIZ = list(res.x)[3] - Qnef_nak
            cormodel.NIZ = list(res.x)[3]
            cormodel.RF_last_fact = Qnef_nak / cormodel.NIZ
        except:
            corey_oil = ["Невозможно"]

        if metka:
            metka_text = '-'
        else:
            metka_text = 'низкое качество данных'

        """Проверка прямых ХВ"""
        if d_set[0] < 0.01 and d_set[1] < 0.01 and metka_text == '-':
            metka_text = 'отброшены точки выше последней'
            New_Wc_fact = Wc_fact[np.where(Wc_fact <= Wc_fact[-1])[0]]
            New_dob_neft = New_dob_neft[np.where(Wc_fact <= Wc_fact[-1])[0]]
            New_dob_zhid = New_dob_zhid[np.where(Wc_fact <= Wc_fact[-1])[0]]

            NIZ = cormodel.OIZ + Qnef_nak
            NIZ_L = cormodel.oiz_left + Qnef_nak
            NIZ_R = cormodel.oiz_right + Qnef_nak
            d_set = [cormodel.corey_oil, cormodel.corey_water, cormodel.mef, NIZ]
            CD = Characteristic_of_Desaturation(New_dob_neft, New_dob_zhid, cormodel.ID, metka, New_Wc_fact,
                                                Qnef_nak, self.bind_to_mean)
            bnds = Bounds([cormodel.corey_oil_left, cormodel.corey_water_left, cormodel.mef_left, NIZ_L],
                            [cormodel.corey_oil_right, cormodel.corey_water_right, cormodel.mef_right, NIZ_R])

            try:
                non_linear_con = NonlinearConstraint(CD.Conditions_CD, [-0.001], [0.001])
                res = minimize(CD.Solver, d_set, method='trust-constr', bounds=bnds, constraints=non_linear_con)
                d_set = res.x
                cormodel.corey_oil = list(res.x)[0]
                cormodel.corey_water = list(res.x)[1]
                cormodel.mef = list(res.x)[2]
                cormodel.OIZ = list(res.x)[3] - Qnef_nak
                cormodel.NIZ = list(res.x)[3]
                cormodel.RF_last_fact = Qnef_nak / cormodel.NIZ
            except:
                corey_oil = ["Невозможно"]


        if (d_set[0] < 0.01 and d_set[1] < 0.01) or corey_oil == ["Невозможно"]:
            metka_text = 'отброшены все точки кроме последней'

            def func(x):
                return -Wc_fact[-1] * x ** 3 + 3 * (2 * Wc_fact[-1] - 1) * x ** 2 - 3 * Wc_fact[-1] * x + Wc_fact[-1]

            niz = oiz_w.loc[0, 'ОИЗ Right'] + Qnef_nak
            RF_new = fsolve(func, np.array(0))
            cormodel.OIZ = Qnef_nak / RF_new[0] - Qnef_nak
            cormodel.NIZ = cormodel.OIZ + Qnef_nak
            cormodel.RF_last_fact = Qnef_nak / cormodel.NIZ

        if cormodel.RF_last_fact is None:
            cormodel.RF_last_fact = Qnef_nak/cormodel.NIZ
        cormodel.metka = metka_text
        return cormodel



class Characteristic_of_Desaturation:
    """Функция характеристики выстеснения"""

    def __init__(self, oil_production, liq_production, name_well, mark, Wc_fact, qnak, binding, RF_now = None, IRR = None):
        self.oil_production = oil_production
        self.liq_production = liq_production
        if IRR is not None:
            self.IRR = IRR
            self.RF_now = RF_now
        else:
            self.IRR = None
            self.RF_now = None
        self.Qnef_nak = qnak
        self.name_well = name_well
        self.mark = mark
        self.Wc_fact = Wc_fact
        self.binding = binding


    def Solver(self, correlation_coeff):
        """
        Апроксимация кривой добычи жидкости - Арпс
        :param correlation_coeff: пареметры корреляции
        :return: сумма квадратов отклонений точек функции от фактических
        """
        corey_oil, corey_water, mef, IRR = correlation_coeff
        v1 = np.cumsum(self.oil_production) / IRR / 1000
        v1 = np.delete(v1, 0)
        v1 = np.insert(v1, 0, 0)
        k1 = (1 - v1) ** corey_oil / ((1 - v1) ** corey_oil + mef * v1 ** corey_water)
        v2 = v1 + self.liq_production * k1 / 2 / IRR / 1000
        k2 = (1 - v2) ** corey_oil / ((1 - v2) ** corey_oil + mef * v2 ** corey_water)
        v3 = v1 + self.liq_production * k2 / 2 / IRR / 1000
        k3 = (1 - v3) ** corey_oil / ((1 - v3) ** corey_oil + mef * v3 ** corey_water)
        v4 = v1 + self.liq_production * k3 / 2 / IRR / 1000
        k4 = (1 - v4) ** corey_oil / ((1 - v4) ** corey_oil + mef * v4 ** corey_water)

        oil_production_model = self.liq_production / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        oil_production_model[oil_production_model == -np.inf] = 0
        oil_production_model[oil_production_model == np.inf] = 0

        deviation = [(oil_production_model - self.oil_production) ** 2]
        return np.sum(deviation)

    def Conditions_CD(self, correlation_coeff):
        """Привязка (binding) к последним фактическим точкам"""
        corey_oil, corey_water, mef, IRR = correlation_coeff
        RF_now = self.Qnef_nak/IRR

        if self.binding:
            point = 3
        else:
            point = 1
        if math.isnan(point) or self.mark == False:
            point = 1
        if point == 1:
            if self.Wc_fact.size > 1:
                Wc_last = self.Wc_fact[-1]
            else:
                Wc_last = self.Wc_fact
        elif point == 3:
            if self.Wc_fact.size >= 3:
                Wc_last = np.average(self.Wc_fact[-3:-1])
            elif self.Wc_fact.size == 2:
                Wc_last = np.average(self.Wc_fact[-2:-1])
            else:
                Wc_last = self.Wc_fact


        Wc_model = mef * RF_now ** corey_water / (
                (1 - RF_now) ** corey_oil + mef * RF_now ** corey_water)
        binding = Wc_model - Wc_last
        return [binding]