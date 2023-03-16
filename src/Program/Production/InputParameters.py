import datetime as dt


class ParametersOfAlgorithm:
    """
    Класс-контейнер исходных параметров алгоритма балансировки (бригады, насосы)
    """

    def __init__(self,
                 value : float = 8000,
                 time_lag_step: int = 3,
                 max_objects_per_day: int = 5,
                 days_per_object: int = 5,
                 cluster_min_liquid: float = 0,
                 max_nrf_objects_per_day: int = 100,
                 pump_extraction_value: float = 0.1,
                 compensation: bool = False,
                 constraints_from_file: bool = False,
                 crew_constraints: dict = {'No constraints': 'No constraints'}
                 ):
        self.value = value
        self.time_lag_step = time_lag_step
        self.max_objects_per_day = max_objects_per_day
        self.days_per_object = days_per_object
        self.cluster_min_liquid = cluster_min_liquid
        #self.max_nrf_object_per_day = max_nrf_objects_per_day
        #self.pump_extraction_value = pump_extraction_value
        self.compensation = compensation
        self.constraints_from_file = constraints_from_file
        self.crew_constraints = crew_constraints


class TimeParameters:
    """
    Класс-контейнер исходных параметров алгоритма балансировки (даты, периоды времени)
    """
    def __init__(self,
                 date_start: dt.date = dt.date(year=2023, month=2, day=1),
                 current_date: dt.date = dt.date(year=2023, month=2, day=1),
                 date_begin: dt.date = dt.date(year=2023, month=2, day=1),
                 date_end: dt.date = dt.date(year=2024, month=1, day=31),
                 time_step: str = 'Month',
                 ):
        self.date_start = date_start
        self.current_date = current_date
        self.date_begin = date_begin
        self.date_end = date_end
        self.time_step = time_step
