from datetime import datetime
from typing import Type, Optional
import numpy as np
from constants import (
    ProductionNames
)


from Tatyana_Prod.Domain.WellDO import WellDo
from Tatyana_Prod.Domain.CircWCModelDO import CircModel

TProductionNames = Type[ProductionNames]


class CircPredictionTechnique():
    '''Класс содержит логику построения модели ХВ по .
        Принимает на вход:
            :param const: ГУ для аргументов функции
            :param binding_period: количество периодов привязки для определения начального дебита.
        Возвращает:
            экземпляр CircModel с оптимизированной функцией
    '''

    def __init__(
            self,
            prod_names: TProductionNames,
            binding_period: int = 3,
            constraints: Optional[np.ndarray]=None,
    ):
        self.prod_names = prod_names
        self.fact_production_column = self.prod_names.StandardCode
        self.binding_period = binding_period
        self.const = constraints


    def calc_wc(self, well: WellDo,
            on_date: datetime,
            ) -> CircModel:

        ''' :param well: объект с информацией по скважине за фактический период
            :param on_date: конечная дата фактической добычи.
            :return: экземпляр класса CircModel, описывающий прогнозную модель добычи жидкости.'''