import numpy as np
import pandas as pd

from Domain.LiqModelDO import LiqModel

class ExpModel(LiqModel):

    def __init__(self):
        exp_coef = None
