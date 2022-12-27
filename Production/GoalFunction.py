class GoalFunction:
    def __init__(self,
                 parameters,
                 results = None,
                 a: int = 200,
                 b: int = 40000000,
                 c: int = 1,
                 ) -> None:
        self.parameters = parameters
        self.results = results
        self.a = a
        self.b = b
        self.c = c
        if self.parameters.days_per_object < 1: self.parameters.days_per_object = 1

    def value(self, target: float = None, results=None):
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
            a = target - results[0]
            if a < 0:
                a = 0
            b = results[1]
            count = self._calculate_turns_on(results[2])
            g = b
            crude = self._calculate_crude_days(results[2])
            goal_function = self.a * a + self.b * (1/g) + self.c * count + crude
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
                    a += (target - results[0][i]) ** 2
            b = results[1]
            count = self._calculate_turns_on(results[2])
            crude = self._calculate_crude_days(results[2])
            g = b

            goal_function = self.a * a + self.b * (1 / g) + self.c * count + crude
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
                    count += (obj_num - self.parameters.max_objects_per_day) ** 2
            except:
                print('Goal function execption')
        return count

    def _calculate_crude_days(self, results: dict):
        keys = list(results.keys())
        crude = 0
        values = list(results.values())
        for i in range(len(results) - self.parameters.days_per_object - 1):
         #   a = 0
          #  for j in range(self.parameters.days_per_object):

            if ((keys[i+1]-keys[i]) > self.parameters.days_per_object) and ((values[i+1]+values[i])>self.parameters.max_objects_per_day):
                crude += 500
        return crude

