import abc
from abc import ABC
from Program.Production.ap_parameters import APParameters
import random
import os
from Program.Production.Logger import Logger
from Program.Production.GoalFunction import GoalFunction
#import pulp as lp
from math import floor


class Optimizator(ABC):
    def __init__(self,
                 parameters: APParameters ):
        self.parameters = parameters

    @abc.abstractmethod
    def __initialization(self):
        pass

    def algorithm(self, index, outParams = None, last_index = None):
        pass
"""
class CbcOptimizator(Optimizator):
    def __init__(self,
                 parameters: APParameters,
                 goal_function: GoalFunction,
                 domain_model,
                 input_parameters = None):
        self.parameters = parameters
        self.goal_function = goal_function
        self.domain_model = domain_model
        self.input_parameters = input_parameters
        self.kids = []

    def __initialization(self):
        model= lp.LpProblem("Balancer", lp.LoMinimize)
        X = lp.LpVariable(self.parameters.inValues())
        model =+ X ==2
        return model

    def algorithm(self):
        solver = lp.PULP_CBC_CMD()
        model = self.__initialization()
        return model.solve(solver)
"""
class GreedyOptimizer():
    def __init__(self,
                 parameters: APParameters,
                 constraints,
                 goal_function: GoalFunction
                 ):
        self.parameters = parameters
        self.constraints = constraints
        self.goal_function = goal_function
        self.max_objects = None
        self.best_kid = []
        self.results = None
        self.last_index = 0
        self.object_count = 0
        self.shift = 0
        self.best = None
        self.solution = False


    def __initialization(self):

        self.object_count = 0
        self.max_objects = self.constraints.max_objects_per_day * \
                           (self.constraints.date_end - self.constraints.current_date -
                            self.constraints.time_lag_step)/(1 + self.constraints.days_per_object)
        print('Initialization')
        if self.best_kid == []:
            self.best_kid.append([])
            for j in range(len(self.parameters.inValues()[0])):
                self.best_kid[0].append(self.parameters.inValues()[0][j])
        return self.best_kid

    def algorithm(self,
                  index,
                  outParams=None,
                  last_index=0,
                  constraints=None
                  ):
        if constraints is not None:
            self.constraints = constraints
        if index == 0:
            return self.__initialization()
        if index == 1:
            if outParams is not None:
                self.results = outParams
            else:
                print('No results in optimizator')
            self.last_index = last_index
            return self.__algorithm()

    def __algorithm(self):

        self.best = self.goal_function.value(results=self.results)
        if self.best != 0 and self.object_count < self.max_objects:
                self.object_count += 1
                a = floor(self.object_count / self.constraints.max_objects_per_day)  # максимальный сдвиг с учетом бригад
                self.shift = a * self.constraints.days_per_object  # максимальный сдвиг с учетом ремонта
                try:
                    for i in range(self.last_index, self.last_index + self.object_count):
                        shift = self.shift-self.constraints.days_per_object*floor((i-self.last_index)/self.constraints.max_objects_per_day)
                        self.best_kid[0][i] = self.constraints.date_end - shift
                except:
                    print('No wells avaliable')
                    self.solution = True

        else:
            self.solution = True


        return self.best_kid










class JayaOptimizator:

    def __init__(self,
                 kids_number,
                 parameters,
                 goal_function: GoalFunction,

                 input_parameters=None
                 ):
        self._logger = Logger('log.txt')
        self._log_ = self._logger.log
        self._resultLog = Logger('ap_jaya_results.txt')
        self._resultLog_ = self._resultLog.log
        self.__iteration = 0  # Iteration for output
        self.parameters = parameters
        self.kids_number = kids_number
        self.goal_function_temp = []
        self.kids = []
        self.kids_temp = []
        self.filepath = os.path.abspath(__file__)
        self.filedir = os.path.dirname(self.filepath)
        self.results = []
        self.best = 0
        self.worst = 0
        self.best_kid = []
        self.worst_kid = []
        self.goal_function = []
        self._initialization_completed = False
        self._log_('[APJaya]: ' + self.__class__.__name__)
        self.input_parameters = input_parameters
        self.last_index = 13
        self.first_index = 0
        self.goal_function_main = goal_function

    def __initialization(self):
        self._log_('[APJaya.__initialization]')
        self._log_(str(self.kids_number))
        for i in range(self.kids_number):
            # self._log_('[APJaya.__initialization begin child]')
            self.kids.append([])
            self.kids_temp.append([])
            for j in range(len(self.parameters.inValues()[0])):
                self.kids_temp[i].append(0)
                """
                if i == 0:
                    self.kids[i].append(
                        self.parameters.inValues()[0][j]
                    )
                 # self.kids[i].append(0)
                """
                #else:
                if i == 0:
                 #   self.kids[i].append(
                #       random.choice([0])
                 #   )
                  self.kids[i].append(random.choice([random.randint(self.first_index, self.last_index), self.last_index]))

                else:
                    if self.last_index > 20:
                        a = self.last_index - 20
                    else:
                        a = 0
                    self.kids[i].append(random.choice([
                    random.randint(a, self.last_index)
                                        ,self.last_index]))


        # self.parameters.inValues() =  self.kids
        self._log_('[APJaya.__initialization] Initialization completed')
        self._resultLog_('Initialization completed')

        return self.kids

    def algorithm(self,
                  index,
                  outParams=None,
                  last_index=None,

                  ):
        self.last_index = last_index

        self._log_('[APJaya.algorithm] index: ' + str(index))
        if (index == 0):
            return self.__initialization()

        else:
            return self.__algorithm(outParams)

    def __restictions(self):
        self._log_('[APJaya] no restrictions')

    def __algorithm(self, outParams):
        self._log_('[APJaya.__algorithm]')
        self.__iteration = self.__iteration + 1
        self._resultLog_('Iteration' + str(self.__iteration) + ' completed')

        self.results = outParams
        if self._initialization_completed == False:
            for j in range(self.kids_number):
                self.goal_function.append(self.goal_function_main.value(results=self.results[j]))
                self.goal_function_temp.append(0)
            self.best = min(self.goal_function)
            self.best_kid = self.kids[self.goal_function.index(self.best)]
            self.worst = max(self.goal_function)
            self.worst_kid = self.kids[self.goal_function.index(self.worst)]
            self._initialization_completed = True

        else:
            for j in range(self.kids_number):
                self.goal_function_temp[j] = self.goal_function_main.value(results=self.results[j])
                if self.goal_function_temp[j] < self.goal_function[j]:
                    self.goal_function[j] = self.goal_function_temp[j]
                    for k in range(len(self.parameters.inValues()[0])):
                        self.kids[j][k] = self.kids_temp[j][k]
            worst_temp = max(self.goal_function)
            for j in range(self.kids_number):
                if self.goal_function[j] < self.best:
                    self.best = self.goal_function[j]
                    self.best_kid = self.kids[self.goal_function.index(self.best)]
                    self._resultLog_('New best')
                if worst_temp < self.worst:
                    self.worst = worst_temp
                    self.worst_kid = self.kids[self.goal_function.index(self.worst)]
        #            self._resultLog_('New worst')
        #self._resultLog_(
        #    'Iteration ' + str(self.__iteration) + ' completed. Goal functions are ' + str(self.goal_function))
        self._resultLog_('Best kid is ' + str(self.goal_function.index(self.best)) + ' ' + str(outParams[(self.goal_function.index(self.best))]))#str(self.best_kid))
        for j in range(self.kids_number):
            for k in range(len(self.parameters.inValues()[0])):
                r1 = random.random()
                r2 = random.random()
               # r1 = 1
               # r2 = 1

                self.kids_temp[j][k] = round(self.kids[j][k] + r1 * (self.best_kid[k] - abs(self.kids[j][k])) - \
                                       r2 * ((self.worst_kid[k] - abs(self.kids[j][k]))))
                if self.kids_temp[j][k] < 0:
                    #self.kids_temp[j][k] = random.choice([0, 1, self.last_index])
                    self.kids_temp[j][k] = 0
                if self.kids_temp[j][k] > self.last_index:
                    self.kids_temp[j][k] = self.last_index

        self._log_('[APJaya.__algorithm] completed')

        return self.kids_temp
