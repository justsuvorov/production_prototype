import abc
import sys
from abc import ABC
import datetime as dt
import numpy as np
from copy import deepcopy
import pandas as pd
from Program.Production.Logger import Logger
from Program.Production.InputParameters import ParametersOfAlgorithm
from Program.Production.PreparedDomainModel import PreparedDomainModel
from Program.Production.CalculationMethods import SimpleOperations
from Program.Production.ExcelResult import ExcelResultPotential
from pathlib import Path
from math import floor
import os.path


class Production(ABC):
    def __init__(self,
                 domain_model: PreparedDomainModel,
                 ):
        self.domain_model = domain_model

    @abc.abstractmethod
    def result(self, path):
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
        self.clusters = None
        self.turn_off_nrf_wells = {}

        self._logger = Logger('Balancer.txt')
        self._log_ = self._logger.log

        self.constraints = None

        self.vbd_index = None
        self.initial_vbd_index = None
        self.temp_value = 1000
        self.result_dates = None
        self.error = False

    def result(self, path):
        self.error = False
        constraints = self.__prepare_data()
        if self.error:
            return
        self._save_initial_results(path)
        self.result_dates = self.optimize(constraints=constraints)[0]
        self.vbd_index = self.initial_vbd_index
        return self.__export_results(path=path)

    def optimize(self, constraints):
        outParams = [[]]
        for iteration in range(self.iterations_count):
            self._log_('iteration index: ' + str(iteration))
            outParams = self._calculate_out_params(iteration=iteration,
                                                   outParams=outParams,
                                                   constraints=constraints)
            if self.optimizer.solution:
                break
        return self.optimizer.best_kid

    def __prepare_data(self):
        self.domain_model, dates = self.prepared_domain_model.recalculate_indicators()
        if not self.domain_model['Wells']:
            self.error = True
        constraints = deepcopy(self.input_parameters)
        self.steps_count = dates['steps_count']
        self.date1 = dates['date1']
        self.date2 = dates['date2']
        self.optimizer.parameters.from_domain_model(objects=self.domain_model['Wells'], last_index=self.date2)
        constraints.date_end = dates['date2']
        constraints.date_begin = dates['date1']
        constraints.current_date = dates['current_date']
        self._find_first_vbd_well()
        self._log_('VBD index', self.vbd_index)
        self.shift = self.input_parameters.time_lag_step + self.input_parameters.days_per_object
        if self.case == 4:
            self.input_parameters.value = 1.005 * SimpleOperations(case=self.case,
                                                                   domain_model=self.domain_model['Wells'],
                                                                   date=self.date1,
                                                                   end_interval_date=self.date2,
                                                                   indicator_name='Добыча нефти, тыс. т'
                                                                   ).cumulative_production(active=True)

            self._log_('Initial cumulative production: ' + str(self.input_parameters.value))
        self.initial_vbd_index = self.vbd_index
        self._log_('Data prepared')
        return constraints

    def _calculate_out_params(self, iteration: int, outParams, constraints, first_iteration: bool = True):
        indicator_names = self.optimizer.parameters.outKeys()
        if iteration == 0:
            # new_values = self.optimizer.algorithm(index=0, last_index=self.date2, constraints=self.constraints)
            new_values = self.optimizer.algorithm(index=0, last_index=self.vbd_index, constraints=constraints)

            for i in range(len(new_values)):
               # if self.input_parameters.constraints_from_file:
               #     new_values[i] = self.__update_values(new_values[i])
                number_of_turnings = self._count_number_of_obj(new_values[i])
                updated_model = self._update_domain_model(new_values[i])
                if first_iteration:
                    outParams.append([])
                    for j in range(len(self.optimizer.parameters.outKeys())):
                        outParams[i].append(SimpleOperations(case=self.case,
                                                             domain_model=updated_model['Wells'],
                                                             date=self.date1,
                                                             end_interval_date=self.date2,
                                                             indicator_name=indicator_names[j]).calculate())
                    outParams[i].append(number_of_turnings)

                    outParams.pop()
                else:
                    for j in range(len(self.optimizer.parameters.outKeys())):
                        outParams[i][j] = SimpleOperations(case=self.case,
                                                           domain_model=updated_model['Wells'],
                                                           date=self.date1,
                                                           end_interval_date=self.date2,
                                                           indicator_name=indicator_names[j]).calculate()
                    outParams[i][2] = number_of_turnings


        else:
            # new_values = self.optimizer.algorithm(index=1, outParams=outParams, last_index=self.date2)
            new_values = self.optimizer.algorithm(index=1, outParams=outParams, last_index=self.vbd_index,
                                                  constraints=constraints)
            for i in range(len(new_values)):
             #   if self.input_parameters.constraints_from_file:
             #       new_values[i] = self.__update_values(new_values[i])
                updated_model = self._update_domain_model(new_values[i])
                number_of_turnings = self._count_number_of_obj(new_values[i])
                for j in range(len(self.optimizer.parameters.outKeys())):
                    outParams[i][j] = SimpleOperations(case=self.case,
                                                       domain_model=updated_model['Wells'],
                                                       date=self.date1,
                                                       end_interval_date=self.date2,
                                                       indicator_name=indicator_names[j]).calculate()
                outParams[i][2] = number_of_turnings
        self._log_(outParams)
        return outParams

    def _update_domain_model(self, values, result: bool = False):
        updated_model = deepcopy(self.domain_model)
        for j in range(self.vbd_index, len(updated_model['Wells'])):
            if not updated_model['Wells'][j].object_info.object_activity:
                if values[j] == self.date2 + 1 and result:
                    values[j] = self.steps_count + 100
                self._update_indicators(object=updated_model['Wells'][j], values=values[j], vbd=True)
        return updated_model

    def _update_indicators(self, object, values, vbd: bool = True):
        for key in object.indicators:
            if key != 'Gap index':

                if vbd:
                    a = np.zeros(values)
                    b = object.indicators[key]
                    c = np.concatenate((a, b))

                else:
                    a = np.zeros(365-values)
                    b = object.indicators[key][0:values]
                    c = np.concatenate((b, a))
                object.indicators[key] = c


    def _count_number_of_obj(self, values):
        values = values[(self.vbd_index + 1):]
        unique, counts = np.unique(values, return_counts=True)

        return dict(zip(unique, counts))

    def _find_first_vbd_well(self):
        for i in reversed(range(len(self.domain_model['Wells']))):
            if self.domain_model['Wells'][i].object_info.object_activity:
                self.vbd_index = i
                break

    def _save_initial_results(self, path):
        self._log_('Exporting initial results')
        ExcelResultPotential.save_initial_results(domain_model=self.domain_model,
                                                  vbd_index=self.vbd_index,
                                                  path=path
                                                  )

    def __export_results(self, path):
        domain_model_with_results = self._update_domain_model(self.result_dates, result=True)
        res = pd.DataFrame(self.result_dates)

        if path is not None:
            res.to_excel(path / 'result_vbd.xlsx')
            if self.turn_off_nrf_wells != {}:
                res2 = pd.Series(data=self.turn_off_nrf_wells)
                res2.to_excel(path / 'results_base.xlsx')
                res.to_excel(path / 'results.xlsx')

        return domain_model_with_results
"""
    def __update_values(self, values):
        groups = len(self.input_parameters.crew_constraints)
        constraints = self.input_parameters.crew_constraints
        if self.optimizer.solution:
            self.temp_dict = {}


        for i in range(self.initial_vbd_index, len(values)):
            if not self.domain_model['Wells'][i].object_info.object_activity:

                constraints[self.domain_model['Wells'][j].object_info.link_list['Field'][0]]

        return updated_model

"""
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
        self.vbd_index = None
        self.result_dates = None
        self.turn_off_nrf_wells = {}
        self.turn_off_max_number = False
        self.pump_extraction_count = 100

    def optimize(self, constraints):
        outParams = [[]]
        temp_value = True
        first_iteration = True
        available_wells = True
        # count = self._count_number_of_pumps()
        for i in range(12):
            if not available_wells:
                break
            k = 0
            if i * 30.43 < constraints.current_date:  # среднее количество дней в месяце
                continue
            if (not self.input_parameters.compensation or (not first_iteration and (
                    self.optimizer.best == 0)) and self.input_parameters.compensation) or first_iteration:
                self._turn_off_nrf_wells(i, temp_value=temp_value)
            temp_value = False
            constraints.date_end = floor(i * 30.43 + 31)
            constraints.current_date = floor(i * 30.43)
            if self.vbd_index >= len(self.domain_model['Wells']):
                break
            self.optimizer.solution = False
            for iteration in range(0, self.iterations_count):
                k += 1
                self._log_('iteration index: ' + str(iteration))
                outParams = self._calculate_out_params(iteration=iteration,
                                                       outParams=outParams,
                                                       constraints=constraints,
                                                       first_iteration=first_iteration)

                if (self.vbd_index >= len(self.domain_model['Wells'])) or self.optimizer.solution:
                    self.vbd_index = self.vbd_index + k - 2
                    break

            first_iteration = False
            if self.vbd_index >= len(self.domain_model['Wells']):
                available_wells = False

        return self.optimizer.best_kid

    def _turn_off_nrf_wells(self, i: int, temp_value: bool = False):
        sum = 0
        wells = self.domain_model['Wells']
        for j in range(self.initial_vbd_index):

            if temp_value:
                if wells[j].indicators['Gap index'] <= i:
                    if self.__check_clusters(wells[j]):
                        sum += 1
                        self.turn_off_nrf_wells[
                            str(wells[j].name[0]) + ' || ' + str(wells[j].object_info.link_list['Field'][0])] = floor(i * 30.43)
                        values = floor(i * 30.43)
                        self._update_indicators(object=wells[j], values=values, vbd=False)

            else:
                if wells[j].indicators['Gap index'] == i:
                    if self.__check_clusters(wells[j]):
                        self.turn_off_nrf_wells[
                            str(wells[j].name[0]) + ' || ' + str(wells[j].object_info.link_list['Field'][0])] = floor(i * 30.43)
                        values = floor(i * 30.43)
                        self._update_indicators(object=wells[j], values=values, vbd=False)
                        sum += 1
            # self.pump_extraction_count -= sum
        self._log_('Выключено ' + str(sum) + ' скважин')

    def __check_clusters(self, well) -> bool:
        result = True
        if isinstance(self.input_parameters.cluster_min_liquid, pd.DataFrame):
            cluster = well.link['Clusters'][0]
            wells = cluster.link['Wells']
            liquid_values = SimpleOperations(case=3,
                                             domain_model=wells,
                                             end_interval_date=365,
                                             indicator_name='Добыча жидкости, тыс. т').calculate()
            try:
                if min(liquid_values) <= self.input_parameters.cluster_min_liquid['Дебит жидкости, тыс. т.'].loc[cluster.name[0]]:
                    result = False
            except:
                pass
        return result
