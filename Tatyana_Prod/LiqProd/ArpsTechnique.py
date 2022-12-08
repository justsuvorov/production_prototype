from datetime import datetime
from typing import Type, Optional
import numpy as np
from scipy.optimize import minimize, Bounds, NonlinearConstraint

from constants import (
    AVG_DAYS_IN_MONTH,
    HOURS_IN_DAY,
    MERNames,
    ProductionNames,
)
from Tatyana_Prod.Domain.WellDO import WellDo
from Tatyana_Prod.Domain.ArpsModelDO import ArpsLModel, ArpsCombLModel
from Tatyana_Prod.arps_function import CombinedArps

TProductionNames = Type[ProductionNames]



class ArpsLiqPredictionTechnique():
    '''Класс содержит логику построения модели добычи жидкости по Арпсу.
        Принимает на вход:
            :param const: ГУ для аргументов функции Арпса
            :param binding_period: количество периодов привязки для определения начального дебита.
            :param polka: полка для жидкости, если 1, то модель не подбирается, а считается как средняя
                            от других скважин
        Возвращает:
            экземпляр ArpsModelDO с оптимизированной функцией Арпса
    '''

    def __init__(
            self,
            prod_names: TProductionNames,
            binding: bool,
            binding_period: int = 3,
            constraints: np.ndarray=None,
            search_gtm = False,
            polka=False,
            double_arps = True
    ):
        self.prod_names = prod_names
        self.fact_production_column = self.prod_names.StandardCode
        self.binding_mean = binding
        self.binding_period = binding_period
        self.const = constraints
        self.search_gtm = search_gtm
        self.polka = polka
        self.double_arps = double_arps



    def main_calc(self, well, start_month):
        if self.double_arps:
            model = self.calc_comb_liq(well, start_month)
        else:
            model = self.calc_liq(well, start_month)
        return model


    def calc_liq(self, well: WellDo,
            on_date: Optional[datetime] = None,
            bf_date: Optional[datetime] = None,
            ) -> ArpsLModel:

        ''' :param well: объект с информацией по скважине за фактический период
            :param on_date: конечная дата фактической добычи.
            :return: экземпляр класса ArpsLModel, описывающий прогнозную модель добычи жидкости.'''

        mer = well.mer.loc[
            (well.mer[MERNames.OIL_PRODUCTION] > 0) & (well.mer[MERNames.LIQUID_PRODUCTION] > 0) \
             & (well.mer[MERNames.OPERATING_TIME_HPM] > 0)]
        dob_zhid = mer[MERNames.LIQUID_PRODUCTION].to_numpy()
        vrem_dob = mer[MERNames.OPERATING_TIME_HPM].to_numpy()

        model = ArpsLModel(well, self.const, self.search_gtm, self.polka)
        model.check_const()
        start_q = dob_zhid[-1]

        if self.polka == True:
            model.k1 = 0
            model.k2 = 1
            return model

        """ Условие, если недостаточно точек для расчёта Арпса"""
        if (dob_zhid.size < 4) :
            #коэффициенты для таких скважин будут рассчитаны на следующем шаге
            start_q = dob_zhid[-1]/(vrem_dob[-1]/24)
            model.start_q_liq = start_q
            model.new_wells = np.array(well)
        else:
            if self.search_gtm == True:
                #поиск точек ГТМ, если они есть, модель считается как средняя между точками
                return model
            model = self.optimize(model, dob_zhid, vrem_dob)

        return model


    def optimize(self, arps_model, dob_zhid, vrem_dob):
        """
        Функция для аппроксимации характеристики вытеснения
        :param arps_model: модель Арпса для апроксимации
        :param dob_zhid: массив дебитов жидкости
        :param vrem_dob: массив времени работы скважины
        :return: output - аппроксимированная модель Арпса
        [k1, k2, first_m, start_q, index, Qnef_nak]
         0  1       2        3       4       5
        """
        dob_zhid_v_cutki = dob_zhid / (vrem_dob / 24)
        c_cet = [arps_model.k1, arps_model.k2]
        FP = FunctionFluidProduction(dob_zhid_v_cutki, arps_model.ID, self.binding_mean, None, None)
        bnds = Bounds([arps_model.k1_left, arps_model.k2_left], [arps_model.k1_right, arps_model.k2_right])
        #try:
        for i in range(10):
            non_linear_con = NonlinearConstraint(FP.Conditions_FP_Arps, [-0.00001], [0.00001])
            res = minimize(FP.Adaptation_Arps, c_cet, method='trust-constr', bounds=bnds, constraints=non_linear_con, options={'disp': False})
            c_cet = res.x
            if res.nit < 900:
                break
        arps_model.k1 = list(res.x)[0]
        arps_model.k2 = list(res.x)[1]
        arps_model.start_q_liq = FP.start_q
        #except:
            #arps_model.k1 = ["Невозможно"]
        return arps_model


    def calc_comb_liq(self, well: WellDo,
            on_date: Optional[datetime] = None,
            bf_date: Optional[datetime] = None,
            ) -> ArpsCombLModel:

        ''' :param well: объект с информацией по скважине за фактический период
            :param on_date: конечная дата фактической добычи.
            :return: экземпляр класса ArpsLModel, описывающий прогнозную модель добычи жидкости.'''

        mer = well.mer.loc[
            (well.mer[MERNames.OIL_PRODUCTION] > 0) & (well.mer[MERNames.LIQUID_PRODUCTION] > 0) \
             & (well.mer[MERNames.OPERATING_TIME_HPM] > 0)]
        dob_zhid = mer[MERNames.LIQUID_PRODUCTION].to_numpy()
        vrem_dob = mer[MERNames.OPERATING_TIME_HPM].to_numpy()

        model = ArpsCombLModel(well, self.const, self.search_gtm, self.polka)

        if self.polka == True:
            return model

        """ Условие, если недостаточно точек для расчёта Арпса"""
        if (dob_zhid.size < 4) :
            #коэффициенты для таких скважин будут рассчитаны на следующем шаге
            start_q = dob_zhid[-1]/(vrem_dob[-1]/24)
            model.start_q = start_q
            model.new_wells = np.array(well)
        else:
            if self.search_gtm == True:
                #поиск точек ГТМ, если они есть, модель считается как средняя между точками
                return model
            model = self.optimize_comb(model, dob_zhid, vrem_dob)

        return model

    def optimize_comb(self, arps_model: ArpsCombLModel,
                      dob_zhid: np.ndarray,
                      vrem_dob: np.ndarray):
        """
        Функция для аппроксимации характеристики вытеснения
        :param arps_model: модель Арпса для апроксимации
        :param dob_zhid: массив дебитов жидкости
        :param vrem_dob: массив времени работы скважины
        :return: output - аппроксимированная модель Арпса
        [k1, k2, first_m, start_q, index, Qnef_nak]
         0  1       2        3       4       5
        """
        dob_zhid_v_cutki = dob_zhid / (vrem_dob / 24)
        acc_time = np.cumsum(vrem_dob) / HOURS_IN_DAY / AVG_DAYS_IN_MONTH
        acc_time = np.insert(acc_time, 0, 0, axis=0)
        integral_liq = np.array(dob_zhid_v_cutki) * (acc_time[1:] - acc_time[:-1])

        c_cet = np.array([arps_model.b1, arps_model.b2, arps_model.D1, arps_model.t])
        FP = FunctionFluidProduction(dob_zhid_v_cutki, arps_model.ID, self.binding_mean, acc_time, integral_liq)
        bnds = Bounds([0.000001, 0.000001, 0.000001, 5], [50, 0.9999, 0.9999, 100])

        try:
            non_linear_con = NonlinearConstraint(FP.Conditions_FP_CombArps, [-0.001], [0.001])
            res = minimize(FP.Adaptation_CombArps, x0=c_cet, method='trust-constr',  bounds=bnds,  constraints=non_linear_con)
            #res = minimize(FP.Adaptation_CombArps, x0=c_cet,  bounds=bnds, args=(acc_time, acc_liq))
            arps_model.b1 = list(res.x)[0]
            arps_model.b2 = list(res.x)[1]
            arps_model.D1 = list(res.x)[2]
            arps_model.t = list(res.x)[3]
            arps_model.start_q = np.amax(dob_zhid_v_cutki)
            c_cet = res.x
        except:
            print('!!!!!!!!!' + str(arps_model.ID) + '   fails to bind')
            non_linear_con = NonlinearConstraint(FP.Conditions_FP_CombArps, [-1], [1])
            res = minimize(FP.Adaptation_CombArps, x0=c_cet, method='trust-constr', bounds=bnds, constraints=non_linear_con)
            arps_model.b1 = list(res.x)[0]
            arps_model.b2 = list(res.x)[1]
            arps_model.D1 = list(res.x)[2]
            arps_model.t = list(res.x)[3]
            arps_model.start_q = np.amax(dob_zhid_v_cutki)
            c_cet = res.x

        integral = CombinedArps.calc_integral(acc_time[acc_time.size - 2], acc_time[acc_time.size-1], *c_cet)
        integral2 = CombinedArps.calc_integral(acc_time[acc_time.size - 1], acc_time[acc_time.size-1]+1, *c_cet)
        q_last = integral * arps_model.start_q/(acc_time[acc_time.size - 1] - acc_time[acc_time.size - 2])
        q_next_to_last = arps_model.start_q * integral2
        bind = np.average(dob_zhid_v_cutki[-3:])
        return arps_model


class FunctionFluidProduction:
    """Функция добычи жидкости"""

    def __init__(self, day_fluid_production, name_well, bind, cummtime, cummprod):
        self.day_fluid_production = day_fluid_production
        self.cummtime = cummtime
        self.cummprod = cummprod
        self.new_well = name_well
        self.binding_mean = bind
        self.first_m = -1
        self.start_q = -1
        self.ind_max = -1

    def Adaptation_Arps(self, correlation_coeff):
        """
        :param correlation_coeff: коэффициенты корреляции функции
        :return: сумма квадратов отклонений фактических точек от модели
        """
        k1, k2 = correlation_coeff
        max_day_prod = np.amax(self.day_fluid_production)
        index = list(np.where(self.day_fluid_production == np.amax(self.day_fluid_production)))[0][0]
        if index != (self.day_fluid_production.size - 1) and \
                index > (self.day_fluid_production.size - 4) and \
                self.day_fluid_production.size > 3:

            if self.binding_mean:
                point = 3
            else:
                point = 1
            if point == 1:
                base_correction = self.day_fluid_production[-1]
            elif point == 3:
                if self.day_fluid_production.size >= 3:
                    base_correction = np.average(self.day_fluid_production[-3:-1])
                elif self.day_fluid_production.size == 2:
                    base_correction = np.average(self.day_fluid_production[-2:-1])
                else:
                    base_correction = self.day_fluid_production[-1]
            if base_correction < np.amax(self.day_fluid_production[:-3]):
                max_day_prod = np.amax(self.day_fluid_production[:-3])
                index = list(np.where(self.day_fluid_production == np.amax(self.day_fluid_production[0:-3])))[0][0]

        indexes = np.arange(start=index, stop=self.day_fluid_production.size, step=1) - index
        day_fluid_production_month = max_day_prod * (1 + k1 * k2 * indexes) ** (-1 / k2)
        deviation = [(self.day_fluid_production[index:] - day_fluid_production_month) ** 2]
        self.first_m = self.day_fluid_production.size - index + 1
        self.start_q = max_day_prod
        self.ind_max = index
        return np.sum(deviation)

    def Conditions_FP_Arps(self, correlation_coeff):
        """Привязка (binding) к последним фактическим точкам"""
        k1, k2 = correlation_coeff
        global base_correction

        if self.binding_mean:
            point = 3
        else:
            point = 1
        if point == 1:
            base_correction = self.day_fluid_production[-1]
        elif point == 3:
            if self.day_fluid_production.size >= 3:
                base_correction = np.average(self.day_fluid_production[-3:-1])
            elif self.day_fluid_production.size == 2:
                base_correction = np.average(self.day_fluid_production[-2:-1])
            else:
                base_correction = self.day_fluid_production[-1]

        max_day_prod = np.amax(self.day_fluid_production)
        index = list(np.where(self.day_fluid_production == np.amax(self.day_fluid_production)))[0][0]

        if index > (self.day_fluid_production.size - 4) and self.day_fluid_production.size > 3:
            if base_correction < np.amax(self.day_fluid_production[:-3]):
                max_day_prod = np.amax(self.day_fluid_production[:-3])
                index = list(np.where(self.day_fluid_production == np.amax(self.day_fluid_production[0:-3])))[0][0]

        last_prod = max_day_prod * (1 + k1 * k2 * (self.day_fluid_production.size - 1 - index)) ** (-1 / k2)
        binding = base_correction - last_prod
        return binding

    def Adaptation_CombArps(self, x: np.ndarray) -> float:
        """Возвращает значение функции невязки.

        Принимает:
        - x - параметры аппроксимирующей функции;
        - x_well - массив времен в месяцах;
        - y_well - массив добычи нефти за текущий средний месяц.
        """
        values_func = []
        for i in range(len(self.cummtime) - 1):
            values_func.append(CombinedArps.calc_integral(self.cummtime[i], self.cummtime[i + 1], *x))
        #a = sum(y_well) / sum(values_func)
        if np.isnan(values_func).any():
            values_func = []
            #for i in range(len(self.cummtime) - 1):
                #values_func.append(CombinedArps.calc_integral(self.cummtime[i], self.cummtime[i + 1], *x))
        a = np.amax(self.day_fluid_production)
        sub = self.cummprod - a * np.array(values_func)
        #sub = self.day_fluid_production - a * np.array(values_func)
        residual = sum(np.multiply(sub, sub))
        return residual


    def Conditions_FP_CombArps(self, x: np.ndarray):
        """Привязка (binding) к последним фактическим точкам"""
        #t, b1, b2, d1 = coeff
        global base_correction

        if self.binding_mean:
            point = 3
        else:
            point = 1
        if point == 1:
            base_correction = self.day_fluid_production[-1]
        elif point == 3:
            if self.day_fluid_production.size >= 3:
                base_correction = np.average(self.day_fluid_production[-3:])
            elif self.day_fluid_production.size == 2:
                base_correction = np.average(self.day_fluid_production[-2:-1])
            else:
                base_correction = self.day_fluid_production[-1]


        max_day_prod = np.amax(self.day_fluid_production)
        index = list(np.where(self.day_fluid_production == np.amax(self.day_fluid_production)))[0][0]

        if index > (self.day_fluid_production.size - 4) and self.day_fluid_production.size > 3:
            if base_correction < np.amax(self.day_fluid_production[:-3]):
                max_day_prod = np.amax(self.day_fluid_production[:-3])
                index = list(np.where(self.day_fluid_production == np.amax(self.day_fluid_production[0:-3])))[0][0]

        integral =  CombinedArps.calc_integral(self.cummtime[self.cummtime.size - 2 - index], self.cummtime[self.cummtime.size - 1 - index], *x)
        last_prod = max_day_prod * integral/(self.cummtime[self.cummtime.size - 1 - index] - self.cummtime[self.cummtime.size - 2 - index])
        binding = base_correction - last_prod
        return binding