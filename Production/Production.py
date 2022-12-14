import abc
from abc import ABC
import datetime as dt
import numpy as np
from copy import deepcopy


import pandas as pd

from Production.CalculationMethods import *
from Production.Optimizator import *
from Production.goal_function import goal_function
from Production.InputParameters import InputParameters

class Production(ABC):
    def __init__(self,
                 domain_model,
                 ):
        self.domain_model = domain_model

    @abc.abstractmethod
    def result(self):
        pass


class ProductionOnValueBalancer(Production):
    def __init__(self,
                 case: int,
                 input_parameters: InputParameters,
                 optimizator: Optimizator,
                 domain_model,
                 iterations_count: int
                 ):
        self.case = case
        self.input_parameters = input_parameters
        self.optimizer = optimizator
        self.domain_model = domain_model
        self.iterations_count = iterations_count
        self.date1 = None
        self.date2 = None
        self.steps_count = None
        self.date_start = None

    def result(self):

        self._discretizate_parameters()
        self.optimizer.parameters.from_domain_model(self.domain_model[0], last_index=self.steps_count)
        results = self.optimize()
        res = pd.DataFrame(results)
        res.to_excel('res.xlsx')

    def _discretizate_parameters(self):
        time_step = self.input_parameters.time_step

        if time_step == 'Day':
            self.steps_count = 366
            self.date1 = (self.input_parameters.date_begin - self.input_parameters.date_start).days
            self._recalculate_indicators(step=30)
            if self.input_parameters.date_end is not None:
                self.date2 = (self.input_parameters.date_end - self.input_parameters.date_start).days
            else:
                self.date2 = self.steps_count
                print('date2 is the end of the period ')

        if time_step == 'Month':
            self.steps_count = 13
            self.date1 = (self.input_parameters.date_begin.month - self.input_parameters.date_start.month)
            if self.input_parameters.date_end is not None:
                self.date2 = (self.input_parameters.date_end.month - self.input_parameters.date_start.month)
            else:
                self.date2 = self.steps_count
                print('date2 is the end of the period ')

        if time_step == 'Week':
            self.steps_count = 55
            self._recalculate_indicators(step=3)

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

            self.date1 = find_weeks(self.input_parameters.date_begin, self.input_parameters.date_start)
            if self.input_parameters.date_end is not None:
                self.date2 = find_weeks(self.input_parameters.date_end, self.input_parameters.date_start)
            else:
                self.date2 = self.steps_count
                print('date2 is the end of the period ')


    def _recalculate_indicators(self, step: int):
        for object in self.domain_model[0]:
            for key in object.indicators:
                try:
                    l = (object.indicators[key].size - 1) * step + 1  # total length after interpolation
                    np.interp(np.arange(l), np.arange(l, step=step), object.indicators[key])  # interpolate
                except:
                    print('Cannot recalculate indicators for well ', object.name)

    def optimize(self):
        outParams = [[]]
        for iteration in range(self.iterations_count):
           print('iteration index: ' + str(iteration))
           outParams = self._calculate_out_params(iteration=iteration,
                                                  outParams=outParams)
        print(self.optimizer.best)
        return self.optimizer.best_kid

    def _update_domain_model_activity(self, values):
        for i in range(len(self.domain_model[0])):
            self.domain_model[0][i].object_info.object_activity = values[i]

    def _calculate_out_params(self, iteration: int, outParams):
        indicator_names = self.optimizer.parameters.outKeys()
        if iteration == 0:
            new_values = self.optimizer.algorithm(index=0)
            for i in range(len(new_values)):
                number_of_turnings = self._count_number_of_obj(new_values[i])
                updated_model = self._update_domain_model(new_values[i])
                outParams.append([])
                for j in range(len(self.optimizer.parameters.outKeys())):
                    outParams[i].append(SimpleOperations(case=self.case,
                                                         domain_model=updated_model,
                                                         date=self.date1,
                                                         end_interval_date=self.date2,
                                                         indicator_name=indicator_names[j]).calculate())
                outParams[i].append(number_of_turnings)


            outParams.pop()

        else:
            new_values = self.optimizer.algorithm(index=1, outParams=outParams)
            for i in range(len(new_values)):
                updated_model = self._update_domain_model(new_values[i])
                number_of_turnings = self._count_number_of_obj(new_values[i])

                for j in range(len(self.optimizer.parameters.outKeys())):
                    outParams[i][j] = SimpleOperations(case=self.case,
                                                       domain_model=updated_model,
                                                       date=self.date1,
                                                       end_interval_date=self.date2,
                                                       indicator_name=indicator_names[j]).calculate()
                outParams[i][2] = number_of_turnings
        return outParams

    def _update_domain_model(self, values):
        updated_model = deepcopy(self.domain_model)
        for j in range(len(updated_model[0])):
            if self.domain_model[0].object_info.object_activity == False:
          #  s = values[2000]
                for key in updated_model[0][j].indicators:
                    a = np.zeros(values[j])
                    b = updated_model[0][j].indicators[key]
                    c = np.concatenate((a, b))
                    updated_model[0][j].indicators[key] = c
        return updated_model

    def _count_number_of_obj(self, values):
        values = values[1922:]
        unique, counts = np.unique(values, return_counts=True)
        return(dict(zip(unique, counts)))


