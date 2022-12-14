"""
Created on Fri May 27 16:06:59 2022
@author: Suvorov
"""
from Production.CalculationMethods import SimpleOperations
import numpy as np

def goal_function(results, target=None):
    if target is None: target = 482
   # res = np.sum(results, axis=1)
    a = target - results[0]
    if a < 0: a = 0
    else: a = (target - results[0])**2

    b = 0.000005*results[1]
    count = 0
    for i in range(10):
        try:
            obj_num = results[2][i]
            if obj_num > 5:
                count += obj_num
        except:
            obj_num = 0


    goal_function = a + b + 3 * count

    return round(goal_function, 3)