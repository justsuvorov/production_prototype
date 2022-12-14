class SimpleOperations:
    def __init__(self,
                 domain_model,
                 indicator_name: str,
                 date: int = None,
                 end_interval_date: int = None,
                 ):
        self.domain_model = domain_model
        self.indicator_name = indicator_name
        self.date = date
        self.end_interval_date = end_interval_date


    def wells_sum(self):
        sum = 0
        for object in self.domain_model[0]:
           # if object.object_info.object_activity or not object.object_info.object_activity:
            if self.date is not None:

                 value = object.indicators[self.indicator_name][self.date]
                 sum += value
            else:
                sum += object.indicators[self.indicator_name]
        return round(sum,2)

    def avarage_sum(self):
        sum = 0
        for object in self.domain_model[0]:
            if object.object_info.object_activity:
                if self.date is not None:
                    sum += object.indicators[self.indicator_name][self.date:self.end_interval_date+1]
                else:
                    sum += object.indicators[:self.end_interval_date+1]
        return round(sum.mean(), 2)


class IndicatorsShift:
    def __init__(self,
                 domain_model,
                 indicator_name: str,
                 date: int = None,
                 end_interval_date: int = None,
                 ):
        pass
