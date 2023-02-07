import datetime as dt

class ParametersOfAlgorithm:
    def __init__(self,
                 value: float,
                 time_lag_step: int = None,
                 max_objects_per_day: int = 5,
                 days_per_object: int = 1,
                 max_nrf_objects_per_day: int = 100,
                 pump_extraction_value: float =0.1
                 ):
        self.value = value
        self.time_lag_step = time_lag_step
        self.max_objects_per_day = max_objects_per_day
        self.days_per_object = days_per_object
        self.max_nrf_object_per_day = max_nrf_objects_per_day
        self.pump_extraction_value = pump_extraction_value


class TimeParameters:
    def __init__(self,
                 date_start: dt.datetime = dt.date(year=2022, month=11, day=1),
                 current_date: dt.datetime = dt.date(year=2023, month=2, day=1),
                 date_begin: dt.date = dt.date(year=2022, month=11, day=1),
                 date_end: dt.date = dt.date(year=2023, month=10, day=31),
                 time_step: str = 'Month',
                 type_of_end_date: int = 1 #за скользящий год. 0: за календарный
                 ):
        self.date_start = date_start
        self.current_date = current_date
        self.date_begin = date_begin
        self.date_end = date_end
        self.time_step = time_step
        self.type_of_end_date = type_of_end_date
        if type_of_end_date == 0:
            self.date_end = dt.date(year=2023, month=12, day=31)
