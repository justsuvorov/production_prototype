import datetime as dt

class ValueIndicator:
    def __init(self,
               name: str = None,
               date: dt.datetime = None,
               value: float = None
            ):
        self.name = name
        self.date = date
        self.value = value

class ArrayIndicator:
    def __init(self,
               name: str,
               values,
               dateList: list = None,
               valueList: list = None
    ):
        self.name = name
        self.date = dateList
        self.values = values
        self.value = valueList