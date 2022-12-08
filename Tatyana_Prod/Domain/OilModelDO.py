
import datetime as dt
from typing import Optional
from Tatyana_Prod.Domain.WellDO import WellDo


class OilModel():
    """Класс, характеризующий модель добычи нефти в зависимотсти от жидкости и ХВ
           Принимает на вход:
                   :param ID: идентификатор скважины
                   :param start_month:
                   :param ke:
                   :param gtm_find:
                   :param gtm_substract:
                   :param sum_condensate:
                   :param new_wells: новые скважины, которые работали
                           меньше 4 месяцев и будут расчитаны как среднее от других скважин
                   """

    def __init__(self, well: WellDo,
                 start_month: dt.datetime, end_month: dt.datetime,
                 #use_coef: pd.DataFrame,
                 gtm_find: Optional[bool] = False,
                 gtm_substract:  Optional[bool] = False,
                 sum_condensate: Optional[bool] = False,
                 ):

        self.ID = well.wellID
        self.start_month = start_month
        self.end_month = end_month
        #self.wc_model = wc
        #self.liq_model = liq
        #self.ke = use_coef.loc[self.ID, 'КЭ']

        self.gtm_find = gtm_find
        self.gtm_substract = gtm_substract
        self.sum_condensate = sum_condensate
        self.new_wells = None



