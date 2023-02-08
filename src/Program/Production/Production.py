import abc
from abc import ABC
import datetime as dt
import numpy as np
from copy import deepcopy
import pandas as pd
from Program.Production.Logger import Logger
from Program.Production.InputParameters import ParametersOfAlgorithm
from Program.Production.PreparedDomainModel import PreparedDomainModel
from Program.Production.CalculationMethods import SimpleOperations
from pathlib import Path
from math import floor
import os.path

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
        self.turn_off_nrf_wells = {}

        self._logger = Logger('Balancer.txt')
        self._log_ = self._logger.log

        self.constraints = None

        self.vbd_index = None
        self.initial_vbd_index = None
        self.temp_value = 1000
        self.result_dates = None

    def result(self, path):
        constraints = self.__prepare_data()
        self.initial_vbd_index = self.vbd_index
        if not os.path.exists(path/'initial_results.xlsx'):
            self._save_initial_results(path)
        result_dates = self.optimize(constraints=constraints)
        self.result_dates = result_dates[0]
        self.vbd_index = self.initial_vbd_index
        domain_model_with_results = self._update_domain_model(result_dates[0], result=True)

        res = pd.DataFrame(result_dates)

        if path is not None:
            res.to_excel(path/'result_vbd.xlsx')
            if self.turn_off_nrf_wells != {}:
                res2 = pd.Series(data=self.turn_off_nrf_wells)
                res2.to_excel(path/'results_base.xlsx')
                res.to_excel(path / 'results.xlsx')

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
        self._log_('VBD index', self.vbd_index)
        self.shift = self.input_parameters.time_lag_step + self.input_parameters.days_per_object
        if self.case == 4:
            self.input_parameters.value = 1.005 * SimpleOperations(case=self.case,
                                                                   domain_model=self.domain_model,
                                                                   date=self.date1,
                                                                   end_interval_date=self.date2,
                                                                   indicator_name='Добыча нефти, тыс. т'
                                                                   ).cumulative_production(active=True)

            self._log_('Initial cumulative production: ' + str(self.input_parameters.value))

        self._log_('Data prepared')
        return constraints

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

    def _update_domain_model_activity(self, values):
        for i in range(len(self.domain_model)):
            self.domain_model[i].object_info.object_activity = values[i]

    def _calculate_out_params(self, iteration: int, outParams, constraints, first_iteration: bool = True):
        indicator_names = self.optimizer.parameters.outKeys()
        if iteration == 0:

            #new_values = self.optimizer.algorithm(index=0, last_index=self.date2, constraints=self.constraints)
            new_values = self.optimizer.algorithm(index=0, last_index=self.vbd_index, constraints=constraints)
            for i in range(len(new_values)):
                number_of_turnings = self._count_number_of_obj(new_values[i])
                updated_model = self._update_domain_model(new_values[i])
                if first_iteration:
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
                    for j in range(len(self.optimizer.parameters.outKeys())):
                        outParams[i][j] = SimpleOperations(case=self.case,
                                                           domain_model=updated_model,
                                                           date=self.date1,
                                                           end_interval_date=self.date2,
                                                           indicator_name=indicator_names[j]).calculate()
                    outParams[i][2] = number_of_turnings


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
        self._log_(outParams)
        return outParams

    def _update_domain_model(self, values, result: bool = False):
        updated_model = deepcopy(self.domain_model)
        for j in range(self.vbd_index, len(updated_model)):
            if not updated_model[j].object_info.object_activity:
                try:
                    if values[j] == self.date2+1 and result:
                       values[j] = self.steps_count+100
                except:
                    pass
                    self._log_('Update model exception')
                for key in updated_model[j].indicators:
                    if key != 'Gap index':
                        try:
                            aa = values[j]
                        except:
                            aa = 0
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

    def _save_initial_results(self, path):
        self._log_('Exporting initial results')
        crude_base =[]
        fcf_base = []
        for i in range(self.vbd_index):
            for key in self.domain_model[i].indicators:
                if key == 'Добыча нефти, тыс. т':
                    crude_base.append(self.domain_model[i].indicators[key][0:366])
                if key == 'FCF':
                    fcf_base.append(self.domain_model[i].indicators[key][0:366])
        df = []
        data = [crude_base, fcf_base]
        for table in data:
            df.append(pd.DataFrame(table))
        with pd.ExcelWriter(path/'initial_results.xlsx') as writer:
                df[0].sum(axis=0).to_excel(writer, sheet_name='Production_results_sum')
                df[1].transpose().sum(axis=1).to_excel(writer, sheet_name='Economic_results_base_sum')

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
        #count = self._count_number_of_pumps()
        for i in range(12):
            if not available_wells:
                break

            k = 0
            if i * 30.43 < constraints.current_date: #среднее количество дней в месяце
                continue
            if (not self.input_parameters.compensation or (not first_iteration and (self.optimizer.best == 0)) and self.input_parameters.compensation )  or first_iteration:
                self._turn_off_nrf_wells(i, temp_value=temp_value)
            temp_value = False
            constraints.date_end = floor(i * 30.43 + 31)
            constraints.current_date = floor(i * 30.43)
            if self.vbd_index >= len(self.domain_model):
                break
            self.optimizer.solution = False
            for iteration in range(0, self.iterations_count):
                k += 1
                self._log_('iteration index: ' + str(iteration))
                outParams = self._calculate_out_params(iteration=iteration,
                                                       outParams=outParams,
                                                       constraints=constraints,
                                                       first_iteration=first_iteration)

                if (self.vbd_index >= len(self.domain_model)) or self.optimizer.solution:
                    self.vbd_index = self.vbd_index + k - 2
                    break

            first_iteration = False
            if self.vbd_index >= len(self.domain_model):
                available_wells = False

        return self.optimizer.best_kid

    def _turn_off_nrf_wells(self, i: int, temp_value: bool = False):
        sum = 0
        for j in range(self.initial_vbd_index):
           # if sum >= self.input_parameters.max_nrf_object_per_day and self.input_parameters.compensation:#or sum >= self.pump_extraction_count:
           # if self.input_parameters.compensation:
           #     break
            if temp_value:
                if self.domain_model[j].indicators['Gap index'] <= i:
                    sum += 1
                    self.turn_off_nrf_wells[str(self.domain_model[j].name)+str(self.domain_model[j].object_info.link_list['Field'])] = floor(i * 30.43)
                    for key in self.domain_model[j].indicators:
                        if key != 'Gap index':
                            aa = floor(i*30.43)
                            a = np.zeros(365-aa)
                            b = self.domain_model[j].indicators[key][0:aa]
                            c = np.concatenate((b, a))
                            self.domain_model[j].indicators[key] = c
            else:
                if self.domain_model[j].indicators['Gap index'] == i+1:
                    self.turn_off_nrf_wells[str(self.domain_model[j].name)+str(self.domain_model[j].object_info.link_list['Field'])] = floor(i * 30.43)
                    for key in self.domain_model[j].indicators:
                        if key != 'Gap index':
                            aa = floor(i * 30.43)
                            a = np.zeros(365 - aa)
                            b = self.domain_model[j].indicators[key][0:aa]
                            c = np.concatenate((b, a))
                            self.domain_model[j].indicators[key] = c
                    sum += 1
        #self.pump_extraction_count -= sum
        self._log_('Выключено ' + str(sum) + ' скважин')

    def prepare_results(self, solution):
        pass
"""
    def _count_number_of_pumps(self):
        fcf = SimpleOperations(domain_model=self.domain_model[self.vbd_index:],
                               indicator_name='FCF',
                               case=1,
                               end_interval_date=self.date2
                               ).calculate()
        self.pump_extraction_count = floor(0.5 * fcf/self.input_parameters.pump_extraction_value)
        if self.pump_extraction_count < 0:
            self.pump_extraction_count = 0
            self._log_('No efficient wells')
        else:
            self._log_('Максимальное отключение скважин: ' + str(self.pump_extraction_count))
"""
