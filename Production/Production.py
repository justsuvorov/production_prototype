import abc
from abc import ABC

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
        self.date1=0

    def result(self):
        activity_values = self.optimize()
        res = pd.DataFrame(activity_values)
        res.to_excel('res.xlsx')


    def _create_parameters(self):
        pass

    def optimize(self):
        outParams = [[]]
        for iteration in range(self.iterations_count):
           print('iteration index: ' + str(iteration))
           indicator_names = self.optimizer.parameters.outKeys()
           if iteration == 0:
               new_values = self.optimizer.algorithm(index=0)
               for i in range(len(new_values)):
                   self._update_domain_model(new_values[i])
                   outParams.append([])
                   for j in range(len(self.optimizer.parameters.outKeys())):
                       outParams[i].append(SimpleOperations(domain_model=self.domain_model,
                                                            date=self.date1,
                                                            indicator_name=indicator_names[j]).wells_sum())
               outParams.pop()

           else:
               new_values = self.optimizer.algorithm(index=1, outParams=outParams)
               for i in range(len(new_values)):
                   self._update_domain_model(new_values[i])
                   for j in range(len(self.optimizer.parameters.outKeys())):
                       outParams[i][j] = SimpleOperations(domain_model=self.domain_model,
                                                          date=self.date1,
                                                          indicator_name=indicator_names[j]).wells_sum()
        print(self.optimizer.best)
        return self.optimizer.best_kid

    def _update_domain_model(self, values):
        for i in range(len(self.domain_model[0])):
            self.domain_model[0][i].object_info.object_activity = values[i]


