from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Tuple, Type, List, Optional, Union
from copy import deepcopy
import numpy as np
import pandas as pd
from constants import (
    AVG_DAYS_IN_MONTH,
    HOURS_IN_DAY,
    GTMNames,
    MERNames,
    MetricSIPrefix,
    ProductionNames,
    FundFormationDates
)


from Domain.WellDO import WellDo
from Domain.BLModelDO import BLModel

TProductionNames = Type[ProductionNames]


class BLPredictionTechnique():
    '''Класс содержит логику построения модели добычи жидкости по Арпсу.
        Принимает на вход:

            :param const: ГУ для аргументов функции Б-Л
            :param binding_period: количество периодов привязки для определения начального дебита.
            :param include_fact: будут ли данные факта включены в результат

        Возвращает:
            экземпляр BLModel с оптимизированной функцией Баклея-Леверетта
    '''

    def __init__(
            self,
            prod_names: TProductionNames,
            binding: bool,
            binding_period: int = 3,
            constraints: Optional[np.ndarray]=None,
    ):
        self.prod_names = prod_names
        self.binding_mean = binding
        self.fact_production_column = self.prod_names.StandardCode
        self.binding_period = binding_period
        self.const = constraints

    def calc_liq(self, well: WellDo,
            on_date: datetime,
            bf_date: Optional[datetime] = None,
            ) -> BLModel:

        ''' :param well: объект с информацией по скважине за фактический период
            :param on_date: конечная дата фактической добычи.
            :return: экземпляр класса BLModel, описывающий прогнозную модель добычи жидкости.'''