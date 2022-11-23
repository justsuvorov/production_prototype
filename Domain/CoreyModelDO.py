import numpy as np
import pandas as pd
from typing import Dict, Tuple, Type, List, Optional, Union
from datetime import datetime
from dateutil.relativedelta import relativedelta

from constants import MERNames, StringConstants
from Domain.WellDO import WellDo


class CoreyModel():
    """Класс, характеризующий модель обводнённости по Кори
    Принимает на вход:
            :param ID: идентификатор скважины
            :param corey_oil: коэфициент Кори нефти
            :param corey_water: коэфициент Кори жидкости
            :param mef: модуль динамичности жидкости
            :param corey_oil_left: левая граница коэффициента Кори нефти
            :param corey_water_left: левая граница коэффициента Кори жидкости
            :param mef_left: левая граница модуля
            :param mef_right: правая граница модуля
            :param OIZ: остаточные извлекаемые запасы
            :param NIZ: начальные извлекаемые запасы
            :param RF_last_fact: выработка на последний месяц факта
            :param oiz_left: левая граница ОИЗ
            :param oiz_right: правая граница ОИЗ
            :param metka: способ вычисления ХВ
            """

    def __init__(self, well: WellDo,
                 constants: np.ndarray,
                 oiz: pd.DataFrame(),
                 ):

        self.ID = well.wellID
        self.corey_oil = 3
        self.corey_water = 2
        self.mef = 3

        self.corey_oil_left = constants[0]
        self.corey_water_left = constants[1]
        self.mef_left = constants[2]
        self.mef_right = constants[3]

        self.oiz_left = oiz.loc[0, 'ОИЗ Left']
        self.oiz_right = oiz.loc[0, 'ОИЗ Right']
        self.OIZ = self.oiz_right - (self.oiz_right - self.oiz_left) * 0.5
        self.RF_last_fact = None
        self.NIZ = None
        self.metka = None
        self.q_nak = None


    #поверить, правильно ли заданы ГУ для коэффициентов Кори и модуля
    def check_const(self):
        # Ограничения
        if self.corey_oil_left == 0:
            self.corey_oil_left = 0.00001
        self.corey_oil_right = np.inf

        if self.corey_water_left == 0:
            self.corey_water_left = -np.inf
        self.corey_water_right = np.inf

        if self.mef_left == 0:
            self.mef_left = -np.inf
        if self.mef_right == 0:
            self.mef_right = np.inf


