from datetime import datetime
from typing import Type
import numpy as np
from scipy.optimize import minimize, Bounds, NonlinearConstraint


from constants import (
    AVG_DAYS_IN_MONTH,
    HOURS_IN_DAY,
    MERNames,
    ProductionNames,
)
from Tatyana_Prod.Domain.WellDO import WellDo
from Tatyana_Prod.Domain.ArpsModelDO import ArpsOModel
from Tatyana_Prod.arps_function import CombinedArps


TProductionNames = Type[ProductionNames]



class ArpsPredictionTechnique():
    '''Класс содержит логику построения модели Арпса по эмпирическим данным

    :param binding_period: период привязки
    :param substract_gtm: вычитать ГТМ при прогнозировании.
    :param ret_only_base_prod: при установке в `True` возвращается только БД. Иначе - БД + ГТМ.
    :param account_condensate: учет конденсата нефти.
    :param prepared_aprs_coeffs: расчёт модели по установленным коэффициентам (пока не реализовано)
    '''

    def __init__(self,
                 #prod_names: TProductionNames,
                 binding: bool,
                 binding_period: int = 3,
                 constraints: np.ndarray = None,
                 search_gtm=False,
                 polka=False,
                 ):
        #self.prod_names = prod_names
        #self.fact_production_column = self.prod_names.StandardCode
        self.binding_mean = binding
        self.binding_period = binding_period
        self.const = constraints
        self.search_gtm = search_gtm
        self.polka = polka


    def calc_oil(self, well: WellDo,
                  on_date: datetime,
                  #use_coef: Optional[pd.DataFrame] = None,
                  ) -> ArpsOModel:
        """Расчет помесячной добычи для каждой скважины WellDO.

            :param well: экземпляр класса WellDO.
            :param on_date: конечная дата фактической добычи.
            :param use_coef: предрасчитанный коэффициент эксплуатации.
            :param bf_date: дата формирования базового фонда.
            :return: экземпляр класса ArpsOModel, описывающий прогнозную модель.
            """
        mer = well.mer.loc[
            (well.mer[MERNames.OIL_PRODUCTION] > 0) & (well.mer[MERNames.LIQUID_PRODUCTION] > 0) \
             & (well.mer[MERNames.OPERATING_TIME_HPM] > 0)]
        dob_oil = mer[MERNames.OIL_PRODUCTION].to_numpy()
        vrem_dob = mer[MERNames.OPERATING_TIME_HPM].to_numpy()

        model = ArpsOModel(well, self.search_gtm, self.polka)

        if self.polka == True:
            return model

        """ Условие, если недостаточно точек для расчёта Арпса"""
        if (dob_oil.size < 4) :
            #коэффициенты для таких скважин будут рассчитаны на следующем шаге
            start_q = dob_oil[-1]/(vrem_dob[-1]/24)
            model.start_q_oil = start_q
            model.new_wells = np.array(well)
        else:
            if self.search_gtm == True:
                #поиск точек ГТМ, если они есть, модель считается как средняя между точками
                return model
            model = self.optimize_comb(model, dob_oil, vrem_dob)

        return model


    def optimize_comb(self, arps_model: ArpsOModel,
                      dob_oil: np.ndarray,
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
        dob_oil_v_cutki = dob_oil / (vrem_dob / 24)
        acc_time = np.cumsum(vrem_dob) / HOURS_IN_DAY / AVG_DAYS_IN_MONTH
        acc_time = np.insert(acc_time, 0, 0, axis=0)
        integral_liq = np.array(dob_oil_v_cutki) * (acc_time[1:] - acc_time[:-1])

        c_cet = np.array([arps_model.b1, arps_model.b2, arps_model.D1, arps_model.t])
        FP = FunctionOilProduction(dob_oil_v_cutki, arps_model.ID, self.binding_mean, acc_time, integral_liq)
        bnds = Bounds([0.000001, 0.000001, 0.000001, 5], [50, 0.9999, 0.9999, 100])

        try:
            non_linear_con = NonlinearConstraint(FP.Conditions_FP_CombArps, [-0.001], [0.001])
            res = minimize(FP.Adaptation_CombArps, x0=c_cet, method='trust-constr',  bounds=bnds,  constraints=non_linear_con)
            #res = minimize(FP.Adaptation_CombArps, x0=c_cet,  bounds=bnds, args=(acc_time, acc_liq))
            arps_model.b1 = list(res.x)[0]
            arps_model.b2 = list(res.x)[1]
            arps_model.D1 = list(res.x)[2]
            arps_model.t = list(res.x)[3]
            arps_model.start_q = np.amax(dob_oil_v_cutki)
            c_cet = res.x
        except:
            print('!!!!!!!!!' + str(arps_model.ID) + '   fails to bind')
            non_linear_con = NonlinearConstraint(FP.Conditions_FP_CombArps, [-1], [1])
            res = minimize(FP.Adaptation_CombArps, x0=c_cet, method='trust-constr', bounds=bnds, constraints=non_linear_con)
            arps_model.b1 = list(res.x)[0]
            arps_model.b2 = list(res.x)[1]
            arps_model.D1 = list(res.x)[2]
            arps_model.t = list(res.x)[3]
            arps_model.start_q = np.amax(dob_oil_v_cutki)
            c_cet = res.x

        #integral = CombinedArps.calc_integral(acc_time[acc_time.size - 2], acc_time[acc_time.size-1], *c_cet)
        #integral2 = CombinedArps.calc_integral(acc_time[acc_time.size - 1], acc_time[acc_time.size-1]+1, *c_cet)
        #q_last = integral * arps_model.start_q/(acc_time[acc_time.size - 1] - acc_time[acc_time.size - 2])
        #q_next_to_last = arps_model.start_q * integral2
        #bind = np.average(dob_oil_v_cutki[-3:])
        return arps_model


class FunctionOilProduction:
    """Функция добычи нефти"""

    def __init__(self, day_oil_production, name_well, bind, cummtime, cummprod):
        self.day_oil_production = day_oil_production
        self.cummtime = cummtime
        self.cummprod = cummprod
        self.new_well = name_well
        self.binding_mean = bind
        self.first_m = -1
        self.start_q = -1
        self.ind_max = -1

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
        a = np.amax(self.day_oil_production)
        sub = self.cummprod - a * np.array(values_func)
        #sub = self.day_fluid_production - a * np.array(values_func)
        residual = sum(np.multiply(sub, sub))
        return residual


    def Conditions_FP_CombArps(self, x: np.ndarray):
        """Привязка (binding) к последним фактическим точкам"""
        global base_correction

        if self.binding_mean:
            point = 3
        else:
            point = 1
        if point == 1:
            base_correction = self.day_oil_production[-1]
        elif point == 3:
            if self.day_oil_production.size >= 3:
                base_correction = np.average(self.day_oil_production[-3:])
            elif self.day_oil_production.size == 2:
                base_correction = np.average(self.day_oil_production[-2:-1])
            else:
                base_correction = self.day_oil_production[-1]


        max_day_prod = np.amax(self.day_oil_production)
        index = list(np.where(self.day_oil_production == np.amax(self.day_oil_production)))[0][0]

        if index > (self.day_oil_production.size - 4) and self.day_oil_production.size > 3:
            if base_correction < np.amax(self.day_oil_production[:-3]):
                max_day_prod = np.amax(self.day_oil_production[:-3])
                index = list(np.where(self.day_oil_production == np.amax(self.day_oil_production[0:-3])))[0][0]

        integral =  CombinedArps.calc_integral(self.cummtime[self.cummtime.size - 2 - index], self.cummtime[self.cummtime.size - 1 - index], *x)
        last_prod = max_day_prod * integral/(self.cummtime[self.cummtime.size - 1 - index] - self.cummtime[self.cummtime.size - 2 - index])
        binding = base_correction - last_prod
        return binding
