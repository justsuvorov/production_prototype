"""
Реализация расчета функции Арпса, её модификации и соответствующих им интегралов.
"""
from typing import Union, List
import numpy as np


class Arps:
    """
    Реализация расчета функции Арпса и соответствующего ей определенного интеграла.
    """
    @staticmethod
    def calc(t: Union[float, List[float]], b: float, D: float):
        """
        Расчет значения функции Арпса в точке (точках) `t`.

        :param t: накопленное время.
        :param b: показатель склонения.
        :param D: номинальный темп падения добычи.
        """
        return (1. + b * D * t) ** (-1. / b)

    @staticmethod
    def _calc_integral_func(t: Union[float, List[float]], b: float, D: float):
        """
        Расчет значения первообразной для функции Арпса в точке (точках) `t`.

        :param t: накопленное время.
        :param b: показатель склонения.
        :param D: номинальный темп падения добычи.
        """
        return ((1. + b * D * t) ** (1. - 1. / b)) / ((b - 1.) * D)

    @classmethod
    def calc_integral(cls, lower: float, upper: float, b: float, D: float):
        """
        Расчет значения определенного интеграла от функции Арпса.

        :param lower: нижний предел интегрирования.
        :param upper: верхний предел интегрирования.
        :param b: показатель склонения.
        :param D: номинальный темп падения добычи.
        """
        error1 = cls._calc_integral_func(t=upper, b=b, D=D)
        error2 = cls._calc_integral_func(t=lower, b=b, D=D)
        return cls._calc_integral_func(t=upper, b=b, D=D) - cls._calc_integral_func(t=lower, b=b, D=D)


class CombinedArps:
    """
    Реализация расчета комбинированной функции Арпса и соответствующего ей определенного интеграла.
    """
    @staticmethod
    def _calc_D2(b1: float, b2: float, D1: float, tau: float):
        """
        Расчет коэффициента номинального темпа падения добычи после выхода на установившийся режим.
        :param b1: показатель склонения до выхода на установившийся режим.
        :param b2: показатель склонения после выхода на установившийся режим.
        :param D1: номинальный темп падения добычи до выхода на установившийся режим.
        :param tau: время выхода на установившийся режим.
        """
        D2 = D1 / (1. + D1 * tau * (b1 - b2))
        return D1 if D2 < 0 else D2

    @staticmethod
    def _calc_k(b1: float, b2: float, D1: float, D2: float, tau: float):
        """
        Расчет коэффициента, определяющего стартовый дебит в момент времени `tau`.

        :param b1: показатель склонения до выхода на установившийся режим.
        :param b2: показатель склонения после выхода на установившийся режим.
        :param D1: номинальный темп падения добычи до выхода на установившийся режим.
        :param D2: номинальный темп падения добычи после выхода на установившийся режим.
        :param tau: время выхода на установившийся режим.
        """
        return Arps.calc(tau, b1, D1) / Arps.calc(tau, b2, D2)

    @classmethod
    def calc(cls, t: np.ndarray, b1: float, b2: float, D1: float, tau: float):
        """
        Расчет значения комбинированной функции Арпса в точке (точках) `t`.

        :param t: накопленное время.
        :param b1: показатель склонения до выхода на установившийся режим.
        :param b2: показатель склонения после выхода на установившийся режим.
        :param D1: номинальный темп падения добычи до выхода на установившийся режим.
        :param tau: время выхода на установившийся режим.
        """
        D2 = cls._calc_D2(b1=b1, b2=b2, D1=D1, tau=tau)
        k = cls._calc_k(b1=b1, b2=b2, D1=D1, D2=D2, tau=tau)
        res = np.empty(shape=t.shape)
        cond = t < tau
        res[cond] = Arps.calc(t[cond], b1, D1)
        res[~cond] = k * Arps.calc(t[~cond], b2, D2)
        return res

    @classmethod
    def calc_integral(cls, lower: float, upper: float, b1: float, b2: float, D1: float, tau: float):
        """
        Расчет значения определенного интеграла от комбинированной функции Арпса в точке (точках) `t`.

        :param lower: нижний предел интегрирования.
        :param upper: верхний предел интегрирования.
        :param b1: показатель склонения до выхода на установившийся режим.
        :param b2: показатель склонения после выхода на установившийся режим.
        :param D1: номинальный темп падения добычи до выхода на установившийся режим.
        :param tau: время выхода на установившийся режим.
        """
        D2 = cls._calc_D2(b1=b1, b2=b2, D1=D1, tau=tau)
        if D2 == D1:
            b2 = b1
        k = cls._calc_k(b1=b1, b2=b2, D1=D1, D2=D2, tau=tau)

        if tau > upper:
            return Arps.calc_integral(lower, upper, b1, D1)

        if tau < lower:
            return k * Arps.calc_integral(lower, upper, b2, D2)

        return Arps.calc_integral(lower, tau, b1, D1) + k * Arps.calc_integral(tau, upper, b2, D2)
