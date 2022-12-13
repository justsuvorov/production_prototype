"""
Created on Fri May 27 16:06:59 2022
@author: Suvorov
"""
from Production.CalculationMethods import SimpleOperations
import numpy as np

def goal_function(results, target=None):
    if target is None: target = 700
   # res = np.sum(results, axis=1)

    goal_function = (target - results[0])**2 #+ 0.000000*results[1]

    return round(goal_function, 3)