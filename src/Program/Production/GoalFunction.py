from math import log10, floor
from statistics import median

class GoalFunction:
    def __init__(self,
                 parameters,
                 results = None,
                 a: int = 200,
                 b: int = 0,
                 c: int = 0,
                 ) -> None:
        self.parameters = parameters
        self.results = results

        self.a = a
        self.b = b
        self.c = c
        if self.parameters.days_per_object < 1: self.parameters.days_per_object = 1

    def value(self, target: float = None, results=None):
        if len(results) == 1: results = results[0]


        try:
           if len(results[0]) > 1:
              return self._array_result(target, results)
        except:

           return self._value_result(target, results)

    def _value_result(self, target: float = None, results=None):

        try:
            if target is None:
                target = self.parameters.value
            if results is None:
                results = self.results
            a = (target - results[0])
            if a < 0:
               a = 0
            b = results[1]
            g = b - 10**(floor(10**6 * log10(b))/(10**6))
            #aa = log10(b)
            count = self._calculate_turns_on(results[2])

          #  crude = self._calculate_crude_days(results[2])
            goal_function = self.a * a +  self.b * (1/g) + self.c * count #+ crude

            return round(goal_function, 3)

        except:
            print('Not enough data for goal function calculation. Return 1000')
            return 10000

    def _array_result(self, target: float = None, results=None):
        try:
            if target is None:
                target = self.parameters.value
            if results is None:
                results = self.results
            a = 0

            for i in range(len(results[0])):
                if (target - results[0][i]) > 0:
                 a += (target - results[0][i])
            b = results[1]
            count = self._calculate_turns_on(results[2])
          #  crude = self._calculate_crude_days(results[2])
            g = b - 10**(floor(10**6 * log10(b))/(10**6))

            goal_function = self.a * a + self.b * (1 / g) + self.c * count #+ crude

            return goal_function

        except:
            print('Not enough data for goal function calculation. Return 10000')
            return 10000

    def _calculate_turns_on(self, results: dict):
        count = 0
        # max_index = list(results[2].keys())[-1]
        results_list = list(results.values())
        for i in range(len(results)-1):
            try:
                obj_num = results_list[i]
                if obj_num > self.parameters.max_objects_per_day:
                    count += (1 + obj_num - self.parameters.max_objects_per_day) ** 4
            except:
                print('Goal function exception')
        return count

    def _calculate_crude_days(self, results: dict):
        keys = list(results.keys())
        crude = 0
        values = list(results.values())
        a = keys[-2]-keys[0]
        b = 0
        for i in range(len(results)-1):
            b += values[i]
        if b/a > self.parameters.max_objects_per_day/self.parameters.days_per_object:
            crude += (b/a) ** 4
        return crude

