import abc
from abc import ABC
import datetime as dt
import numpy as np
from copy import deepcopy
import pandas as pd
from Program.Production.Logger import Logger
from Program.Production.InputParameters import ParametersOfAlgorithm
from Program.Production.PreparedDomainModel import PreparedDomainModel
from Program.Production.ExcelResult import ExcelResult
from Program.constants import DATA_DIR
from Program.Production.CalculationMethods import SimpleOperations
from pathlib import Path


class Production(ABC):
    def __init__(self,
                 domain_model: PreparedDomainModel,
                 ):
        self.domain_model = domain_model

    @abc.abstractmethod
    def result(self):
        pass


class OperationalProductionBalancer(Production):
    def __init__(self,
                 case: int,
                 input_parameters: ParametersOfAlgorithm,
                 optimizator,
                 prepared_domain_model: PreparedDomainModel,
                 iterations_count: int
                 ):
        self.case = case
        self.input_parameters = input_parameters
        self.optimizer = optimizator
        self.prepared_domain_model = prepared_domain_model
        self.iterations_count = iterations_count

        self.date1 = None
        self.date2 = None
        self.steps_count = None
        self.constraints = None
        self.date_start = 0
        self.domain_model = None

        self._logger = Logger('log.txt')
        self._log_ = self._logger.log
        self._resultLog = Logger('Balancer_results.txt')
        self._resultLog_ = self._resultLog.log
        self.constraints = None

        self.vbd_index = None
        self.temp_value = 1000
        self.result_dates = None

    def result(self, path):
        constraints = self.__prepare_data()
        result_dates = self.optimize(constraints=constraints)
        self.result_dates = result_dates[0]
        domain_model_with_results = self._update_domain_model(result_dates[0], result=True)
        res = pd.DataFrame(result_dates[0])
        if path is not None:
            res.to_excel(path/'res.xlsx')
        else:
            res.to_excel('res.xlsx')
        return domain_model_with_results

    def __prepare_data(self):
        self.domain_model, dates = self.prepared_domain_model.recalculate_indicators()
        constraints = deepcopy(self.input_parameters)
        self.steps_count = dates['steps_count']
        self.date1 = dates['date1']
        self.date2 = dates['date2']
        self.optimizer.parameters.from_domain_model(objects=self.domain_model, last_index=self.date2)
        constraints.date_end = dates['date2']
        constraints.date_begin = dates['date1']
        constraints.current_date = dates['current_date']
        self._find_first_vbd_well()
        self.shift = self.input_parameters.time_lag_step + self.input_parameters.days_per_object
        return constraints

    def optimize(self, constraints):
        outParams = [[]]
        for iteration in range(self.iterations_count):
           print('iteration index: ' + str(iteration))
           outParams = self._calculate_out_params(iteration=iteration,
                                                  outParams=outParams,
                                                  constraints=constraints)
           if self.optimizer.solution:
            break
        return self.optimizer.best_kid

    def _update_domain_model_activity(self, values):
        for i in range(len(self.domain_model)):
            self.domain_model[i].object_info.object_activity = values[i]

    def _calculate_out_params(self, iteration: int, outParams, constraints):
        indicator_names = self.optimizer.parameters.outKeys()
        if iteration == 0:
            #new_values = self.optimizer.algorithm(index=0, last_index=self.date2, constraints=self.constraints)
            new_values = self.optimizer.algorithm(index=0, last_index=self.vbd_index, constraints=constraints)
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
            #new_values = self.optimizer.algorithm(index=1, outParams=outParams, last_index=self.date2)
            new_values = self.optimizer.algorithm(index=1, outParams=outParams, last_index=self.vbd_index, constraints=constraints)
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
        print(outParams)
        return outParams

    def _update_domain_model(self, values, result: bool = False):
        updated_model = deepcopy(self.domain_model)
        for j in range(self.vbd_index, len(updated_model)):
            if not updated_model[j].object_info.object_activity:
                if values[j] == self.date2+1 and result:
                    values[j] = self.steps_count+100
                for key in updated_model[j].indicators:
                    aa = values[j]
                    a = np.zeros(aa)
                    b = updated_model[j].indicators[key]
                    c = np.concatenate((a, b))
                    updated_model[j].indicators[key] = c

        return updated_model

    def _count_number_of_obj(self, values):
        values = values[(self.vbd_index+1):]
        unique, counts = np.unique(values, return_counts=True)

        return dict(zip(unique, counts))

    def _find_first_vbd_well(self):
        for i in reversed(range(len(self.domain_model))):
            if self.domain_model[i].object_info.object_activity:
                self.vbd_index = i
                break


class CompensatoryProductionBalancer(OperationalProductionBalancer):
    def __init__(self,
                 input_parameters: ParametersOfAlgorithm,
                 optimizator,
                 prepared_domain_model: PreparedDomainModel,
                 iterations_count: int,

                 ):
        super().__init__(
                 case=4,
                 input_parameters=input_parameters,
                 optimizator=optimizator,
                 prepared_domain_model=prepared_domain_model,
                 iterations_count=iterations_count
                        )

        self.date1 = None
        self.date2 = 366
        self.steps_count = None
        self.constraints = None
        self.date_start = 0
        self.domain_model = None

        self._logger = Logger('log.txt')
        self._log_ = self._logger.log
        self._resultLog = Logger('Balancer_results.txt')
        self._resultLog_ = self._resultLog.log
        self.constraints = None

        self.vbd_index = None
        self.temp_value = 1000
        self.result_dates = None