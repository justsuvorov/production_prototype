class GoalFunction:
    def __init__(self,
                 parameters,
                 results = None,
                 ) -> None:
        self.parameters = parameters
        self.results = results

    def value(self, target: float = None, results=None):

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
            b = 0.000005 * results[1]
            count = 0
            for i in range(10):
                try:
                    obj_num = results[2][i]
                    if obj_num > self.parameters.max_objects_per_day:
                        count += obj_num
                except:
                    obj_num = 0

            goal_function = a + b + 3 * count
            return round(goal_function, 3)
        except:
            print('Not enough data for goal function calculation. Return 1000')
            return 10000


