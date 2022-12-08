import numpy as np

from Tatyana_Prod.Domain.OilModelDO import OilModel
from Tatyana_Prod.Domain.LiqModelDO import LiqModel
from Tatyana_Prod.Domain.WellDO import WellDo


class ArpsOModel(OilModel):
    """Класс, характеризующий модель добычи нефти по Арпсу
            Принимает на вход:
                    :param ID: идентификатор скважины
                    :param flood: полка по жидкости = 1, если True
                    :param k1: коэфф. Арпса
                    :param k2: коэфф. Арпса
                    :param k1_left:  коэфф. Арпса
                    :param k1_right:  коэфф. Арпса
                    :param gtm_find: требуется ли искать модель с учетом гтм
                    :param start_q_liq: последняя фактическая добыча жидкости
                    :param new_wells: новые скважины, которые работали
                            меньше 4 месяцев и будут расчитаны как среднее от других скважин
                    """

    def __init__(self, well: WellDo,
                 gtm_find: bool,
                 flood: bool
                 ):
        self.ID = well.wellID
        self.flood = flood
        self.t = 5.5
        self.b1 = 0.737052938
        self.b2 = 0.999
        self.D1 = 0.020762861

        self.bounds = ((0.00001, 50), (0.00001, 0.999), (0.00001, 0.999), (5, 100))

        self.gtm_find = gtm_find
        self.start_q = None
        self.new_wells = None
        self.double_arps = True






class ArpsLModel(LiqModel):
    """Класс, характеризующий модель добычи жидкости по Арпсу
        Принимает на вход:
                :param ID: идентификатор скважины
                :param flood: полка по жидкости = 1, если True
                :param k1: коэфф. Арпса
                :param k2: коэфф. Арпса
                :param k1_left: левая граница коэфф. Арпса
                :param k1_right: правая граница коэфф. Арпса
                :param k2_left: левая граница коэфф. Арпса
                :param k2_right: правая граница коэфф. Арпса
                :param gtm_find: требуется ли искать модель с учетом гтм
                :param start_q_liq: последняя фактическая добыча жидкости
                :param new_wells: новые скважины, которые работали
                        меньше 4 месяцев и будут расчитаны как среднее от других скважин
                """

    def __init__(self, well: WellDo,
                 constants: np.ndarray,
                 gtm_find: bool,
                 flood: bool
                 ):

        self.ID = well.wellID
        self.flood = flood
        self.k1 = 1
        self.k2 = 2

        self.k1_left = constants[4]
        self.k1_right = constants[5]
        self.k2_left = constants[6]
        self.k2_right = constants[7]

        self.gtm_find = gtm_find
        self.start_q = None
        self.new_wells = None
        self.double_arps = False

    # поверить, правильно ли заданы ГУ для коэффициентов Кори и модуля
    def check_const(self):
        # Ограничения
        if self.k1_left == 0:
            #self.k1_left = -np.inf
            self.k1_left = 0.0001
        if self.k1_right == 0:
            self.k1_right = np.inf
            #self.k1_right = 1.1

        if self.k2_left == 0:
            #self.k2_left = -np.inf
            self.k2_left = 0.0001
        if self.k2_right == 0:
            self.k2_right = np.inf
            #self.k2_left = 50



class ArpsCombLModel(LiqModel):
    """Класс, характеризующий модель добычи жидкости по Арпсу
        Принимает на вход:
                :param ID: идентификатор скважины
                :param flood: полка по жидкости = 1, если True
                :param k1: коэфф. Арпса
                :param k2: коэфф. Арпса
                :param k1_left:  коэфф. Арпса
                :param k1_right:  коэфф. Арпса
                :param gtm_find: требуется ли искать модель с учетом гтм
                :param start_q_liq: последняя фактическая добыча жидкости
                :param new_wells: новые скважины, которые работали
                        меньше 4 месяцев и будут расчитаны как среднее от других скважин
                """

    def __init__(self, well: WellDo,
                 constants: np.ndarray,
                 gtm_find: bool,
                 flood: bool
                 ):

        self.ID = well.wellID
        self.flood = flood
        self.t =  5.5
        self.b1 = 0.737052938
        self.b2 =  0.999
        self.D1 = 0.020762861

        self.bounds = ((0.00001, 50), (0.00001, 0.999), (0.00001, 0.999), (5, 100))

        self.gtm_find = gtm_find
        self.start_q = None
        self.new_wells = None
        self.double_arps = True


