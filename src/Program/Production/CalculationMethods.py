import numpy as np
from scipy import integrate
class SimpleOperations:
    def __init__(self,
                 domain_model,
                 indicator_name: str ,
                 date: int = 0,
                 end_interval_date: int = None,
                 case: int = 1,
                 end_year_index: int = 366,
                 ):
        self.domain_model = domain_model
        self.indicator_name = indicator_name
        self.date = date
        self.end_interval_date = end_interval_date
        self.case = case
        self.end_year_index = end_year_index

    def calculate(self):


        if self.case == 1:
            return self.wells_sum()

        if self.case == 2:
            return self.average_sum()

        if self.case == 3:
            return self.polka_sum()


    def wells_sum(self, date: int = None):
        sum = 0.0
        if date is None:
            date = self.date
        if self.indicator_name == 'FCF':
            sum = self.fcf()

        else:
            for object in self.domain_model:
                try:

                        value = object.indicators[self.indicator_name][date]
                        sum += value
                except:
                    print('SimpleOperations. Corrupted data for well ', object.name)
            sum = round(sum, 4)

        return sum

    def average_sum(self):
        if self.indicator_name == 'FCF':
            sum = self.fcf()
        else:
            sum = 0
            for object in self.domain_model:
                try:
                    sum += object.indicators[self.indicator_name][self.date:self.end_interval_date+1]
                except:
                    print('SimpleOperations. Corrupted data for well ', object.name)
            sum = round(sum.mean(),2)
        return sum

    def polka_sum(self):
        if self.indicator_name == 'FCF':
            sum = self.fcf()
        else:
            sum = []
            period = self.end_interval_date+1 - self.date
            date = self.date
            for i in range(period):
                sum.append(self.wells_sum(date=date))
                date += 1

        return sum

    def fcf(self):
        sum = 0
        for object in self.domain_model:
            try:
                value = np.sum(object.indicators[self.indicator_name][0:self.end_year_index])
                sum += value
            except:
                print('SimpleOperations. Corrupted data for well ', object.name)

        return sum


    def wells_gap(self):
        gap = []

        for object in self.domain_model:
            try:
                sum = []
                for i in range(self.end_year_index):
                    value = np.sum(object.indicators[self.indicator_name][0:i])
                    sum.append(value)
                    if i != 0 and sum[i] < sum[i-1]:
                        break
                object.indicators['Gap index'] = i

            except:
                print('SimpleOperations. Corrupted data for well ', object.name)
        return self.domain_model

    def cumulative_production(self):
        sum = 0
        for object in self.domain_model:
            try:
                if object.object_info.object_activity:
                    sum += integrate.simpson(y=object.indicators[self.indicator_name][self.date:self.end_interval_date])
            except:
                print('SimpleOperations. Corrupted data for well ', object.name)
        sum = round(sum,2)
        return sum



