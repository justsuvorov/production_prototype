from datetime import datetime
from typing import Type, Optional
import numpy as np
from constants import (
    ProductionNames
)

from Tatyana_Prod.Domain.WellDO import WellDo
from Tatyana_Prod.Domain.ExpModelDO import ExpModel

TProductionNames = Type[ProductionNames]

class ExpPredictionTechnique():
    '''Класс содержит логику построения модели добычи жидкости по экспоненте.
        Принимает на вход:
            :param const: ГУ для аргументов функции
            :param binding_period: количество периодов привязки для определения начального дебита.
            :param include_fact: будут ли данные факта включены в результат
        Возвращает:
            экземпляр ExpModel с оптимизированной функцией экспоненциального выхода на полку
    '''

    def __init__(
            self,
            prod_names: TProductionNames,
            binding: bool,
            binding_period: int = 3,
            constraints: Optional[np.ndarray] = None,
    ):
        self.prod_names = prod_names
        self.binding_mean = binding
        self.fact_production_column = self.prod_names.StandardCode
        self.binding_period = binding_period
        self.const = constraints

    def calc_liq(self, well: WellDo,
                on_date: datetime,
                bf_date: Optional[datetime] = None,
                ) -> ExpModel:

        ''' :param well: объект с информацией по скважине за фактический период
            :param on_date: конечная дата фактической добычи.
            :return: экземпляр класса ExpModel, описывающий прогнозную модель добычи жидкости.'''