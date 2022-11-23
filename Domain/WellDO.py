import numpy as np
import pandas as pd
from typing import Dict, Tuple, Type, List, Optional, Union
from datetime import datetime
from dateutil.relativedelta import relativedelta

from constants import (
    AVG_DAYS_IN_MONTH,
    HOURS_IN_DAY,
    MERNames,
)
import calendar

from constants import StringConstants as SC


class WellDo():
    """Класс, характеризующий добывающую скважину
    Принимает на вход:
            :param ID: идентификатор скважины
            :param mer: месячные отчёты по скважине.
            :param bf_date: дата формирования фонда
            :param character: характер работы скважины (нефтедобывающая,газодобывающая и тд)
            :param in_use: работала ли скважина в один из месяцев за период привязки"""

    def __init__(self,
                 ID ,
                 mer: pd.DataFrame,
                 bf_date: Optional[datetime]=None,
                 character: Optional[str] = 'oil',
                 in_use: Optional[bool] = True):

        self.wellID = ID
        self.field = mer.loc[ID, SC.FIELD][0]
        mer = mer.loc[:, [MERNames.DATE, MERNames.LAYER, MERNames.OPERATING_TIME_HPM,\
                       MERNames.OIL_PRODUCTION, MERNames.LIQUID_PRODUCTION,\
                       MERNames.GAS_PRODUCTION, MERNames.CONDENSATE_OIL_PRODUCTION, \
                        MERNames.GAS_PRODUCTION_FROM_GAS_CAP]]
        mer = mer.loc[mer[MERNames.OIL_PRODUCTION] > 0]
        self.mer = mer.groupby([MERNames.DATE], as_index=False).sum()
        self.mer = self.mer.set_index(np.array([ID for i in self.mer.index]))

        if bf_date is not None:
            self.bf_date = bf_date
        if character is not None:
            self.character = character
        if in_use is not None:
            self.in_use = in_use

        self.prediction_oil = None
        self.prediction_liq = None
        self.prediction_wc = None
        self.prediction_gas = None
        vrem_d = mer.set_index(MERNames.DATE)
        self.time = vrem_d[MERNames.OPERATING_TIME_HPM]

        self.NIZ = None
        self.OIZ = None
        self.OIZ_end = None

        self.ke = 1
        #добавить в МЭР
        self.cummtime = None


    #получить значение, работала ли скважина в один из трех последних месяцев факта
    def get_state(self, last_fact_date: datetime):
        last_mer_date = self.mer.loc[:, MERNames.DATE][-1]
        if (last_fact_date - relativedelta(months=3)) <= last_mer_date:
            self.in_use = True
        else:
            self.in_use = False

    #задать значение, работала ли скважина в один из трех последних месяцев факта
    def set_state(self, state: bool):
        self.in_use = state


    #задать характер добывающей скважины
    def set_character(self, character):
        self.character = character

    def get_ke(self, ke):
        self.ke = ke.loc[self.wellID, 'КЭ']








