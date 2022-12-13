import datetime as dt

class InputParameters:
    def __init__(self,
                 value: float,
                 date_begin: dt.date = None,
                 date_end: dt.date = None,
                 time_step: str = 'Month',
                 ):
        self.value = value
        self.date_begin = date_begin
        self.date_end = date_end
        self.time_step = time_step


