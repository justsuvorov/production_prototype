class SimpleOperations:
    def __init__(self,
                 domain_model,
                 indicator_name: str,
                 date: int = 0,
                 end_interval_date: int = None,
                 case: int = 1
                 ):
        self.domain_model = domain_model
        self.indicator_name = indicator_name
        self.date = date
        self.end_interval_date = end_interval_date
        self.case = case

    def calculate(self):

        if self.case == 1:
            return self.wells_sum()

        if self.case == 2:
            return self.average_sum()

        if self.case == 3:
            return self.polka_sum()


    def wells_sum(self, date: int = None):
        sum = 0
        if date is None:
            date = self.date
        for object in self.domain_model[0]:
            try:
                value = object.indicators[self.indicator_name][date]
                sum += value
            except:
                print('SimpleOperations. Corrupted data for well ', object.name)

        return round(sum, 2)

    def average_sum(self):
        sum = 0
        for object in self.domain_model[0]:
            try:
                sum += object.indicators[self.indicator_name][self.date:self.end_interval_date+1]
            except:
                print('SimpleOperations. Corrupted data for well ', object.name)
        return round(sum.mean(), 2)

    def polka_sum(self):
        sum = []
        period = self.end_interval_date - self.date
        date = self.date
        for i in range(period):
            sum.append(self.wells_sum(date=date))
            date += 1

        return sum



