class GoalFunction:
    def __init__(self,
                 parameters,
                 results = None,
                 ) -> None:
        self.parameters = parameters
        self.results = results


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
            else:
                a = (target - results[0]) ** 2
            b = 0.00000001 * results[1]
            count = 0
            max_index = list(results[2].keys())[-1]
            for i in range(max_index):
                try:
                    obj_num = results[2][i]
                    if obj_num > self.parameters.max_objects_per_day:
                        count += obj_num
                except:
                    obj_num = 0

            goal_function = 100 * a + 1/b + 3 * count
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
            b = 0
            for i in range(len(results[0])):
                if (target - results[0][i]) > 0:
                    a += (target - results[0][i]) ** 2
            b += 0.00000001 * results[1]
            count = 0
            max_index = list(results[2].keys())[-1]
            for i in range(max_index):
                try:
                    obj_num = results[2][i]
                    if obj_num > self.parameters.max_objects_per_day:
                        count += obj_num
                except:
                    obj_num = 0

            goal_function = 100 * a + 1/b + 3 * count
            return round(goal_function, 3)

        except:
            print('Not enough data for goal function calculation. Return 1000')
            return 10000