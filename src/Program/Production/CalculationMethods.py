import numpy as np
from scipy import integrate


class SimpleOperations:
    """
    Класс простых вычислений показателей для доменной модели.

    inputs:
    domain_model: доменная модель в виде !!списка!! (list) объектов
    indicator_name: имя показателя, по которыму выполнить операцию
    data: дата в виде индекса показателя
    end_interval_date: дата в виде индекса показателя до которого производить вычисление
    case: переключатель для метода calculate(). используется в балансировщике.
            1 - вычисление суммы показателей в дату ("Точка")
            2 - вычисление среднего за период ("интеграл")
            3 - вычисление показателей за период  в виде массива("полка")
            4 - вычисление накопленной суммы показателей (интеграл под кривой)
    end_year_index : дата в виде индекса окончания года (календарный или скользящий)

    :returns
    calculate() : метод вызывается внутри балансировщика. возвращает результат вычисления требуемого показателя за период
    wells_gap() : вычисление ГЭП для объекта доменной модели. Результат записывает в доменную модель в словарь Indicators



    """
    def __init__(self,
                 domain_model,
                 indicator_name: str,
                 date: int = 0,
                 end_interval_date: int = 12,
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

        if self.case == 4:
            return self.cumulative_production()

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
            sum = round(sum.mean(), 2)
        return sum

    def polka_sum(self):
        if self.indicator_name == 'FCF':
            sum = self.fcf()
        else:
            sum = []
            period = self.end_interval_date - self.date
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

        for object in self.domain_model:
            try:
                sum = []
                for i in range(self.end_year_index+1):
                    k = i
                    sum.append(np.sum(object.indicators[self.indicator_name][0:k]))
                    if i == 0 and sum[i] < 0:
                        object.indicators['Gap index'] = 0
                        break
                object.indicators['Gap index'] = sum.index(max(sum))

            except:
                print('SimpleOperations. Corrupted data for well ', object.name)
        return self.domain_model

    def cumulative_production(self, active=False):
        sum = 0
        for object in self.domain_model:
            try:
                if not active:
                    sum += integrate.trapezoid(dx=1,
                                               y=object.indicators[self.indicator_name][self.date:self.end_interval_date])
                else:
                    if object.object_info.object_activity:
                        sum += integrate.trapezoid(dx=1,
                                                   y=object.indicators[self.indicator_name][
                                                     self.date:self.end_interval_date+1])

            except:
                print('SimpleOperations. Corrupted data for well ', object.name)
        sum = round(sum, 2)
        return sum


class HierarchyIndicatorsTransfer:
    def __init__(self,
                 domain_model: list):
        self.domain_model = domain_model

