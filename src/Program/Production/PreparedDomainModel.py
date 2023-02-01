from copy import deepcopy
from Program.Production.InputParameters import TimeParameters
import datetime as dt
import numpy as np
from Program.Production.CalculationMethods import SimpleOperations


class PreparedDomainModel:
    def __init__(self,
                 domain_model,
                 time_parameters: TimeParameters,
                 find_gap: bool = False
                 ):
        self.domain_model = domain_model
        self.time_parameters = time_parameters
        self.steps_count = None
        self.find_gap = find_gap
        
    def recalculate_indicators(self):
        domain_model = self.__copy_domain_model()
        if self.find_gap:
            SimpleOperations(domain_model=domain_model,
                             indicator_name='FCF',
                             ).wells_gap()

        time_parameters = self._discretizate_parameters(domain_model=domain_model)
        return domain_model, time_parameters

    def __copy_domain_model(self):
        return deepcopy(self.domain_model[0])
        
    def _discretizate_parameters(self, domain_model):
        time_step = self.time_parameters.time_step

        if time_step == 'Day':
            steps_count = 366
            date1 = (self.time_parameters.date_begin - self.time_parameters.date_start).days
            self._recalculate_indicators(step=30, domain_model=domain_model)
            if self.time_parameters.date_end is not None:
                date2 = (self.time_parameters.date_end - self.time_parameters.date_start).days

            else:
                date2 = self.steps_count
                print('date2 is the end of the period ')

        if time_step == 'Month':
            steps_count = 13
            a = ((self.time_parameters.date_begin.year - self.time_parameters.date_start.year) * 12) +\
                self.time_parameters.date_begin.month - self.time_parameters.date_start.month
            date1 = a
            if self.time_parameters.date_end is not None:
                b = ((self.time_parameters.date_end.year - self.time_parameters.date_start.year) * 12) + \
                    self.time_parameters.date_end.month - self.time_parameters.date_start.month
                date2 = b
            else:
                date2 = self.steps_count
                print('date2 is the end of the period ')

        if time_step == 'Week':
            steps_count = 55
            self._recalculate_indicators(step=3, domain_model=domain_model)

            def find_weeks(start_date, end_date):
                subtract_days = start_date.isocalendar()[2] - 1
                current_date = start_date + dt.timedelta(days=7 - subtract_days)
                weeks_between = []
                while current_date <= end_date:
                    weeks_between.append(
                        '{}{:02d}'.format(*current_date.isocalendar()[:2])
                    )
                    current_date += dt.timedelta(days=7)
                return weeks_between

            date1 = find_weeks(self.time_parameters.date_begin, self.time_parameters.date_start)
            if self.time_parameters.date_end is not None:
                date2 = find_weeks(self.time_parameters.date_end, self.time_parameters.date_start)
            else:
                date2 = self.steps_count
                print('date2 is the end of the period ')
        current_date = (self.time_parameters.current_date - self.time_parameters.date_start).days

        return {'date1': date1, 'date2': date2,  'steps_count': steps_count, 'current_date': current_date}


    def _recalculate_indicators(self, step: int, domain_model):
        for object in domain_model:
            try:
                for key in object.indicators:
                    if key != 'Gap index':
                        try:
                            l = (object.indicators[key].size - 1) * step + 1  # total length after interpolation
                            c = np.array(object.indicators[key]).astype(float)
                            c = c/step
                            a = np.interp(np.arange(l), np.arange(l, step=step), c)  # interpolate
                            object.indicators[key] = a

                        except:
                            print('Cannot recalculate indicators for well ', object.name)
            except:
                print()

