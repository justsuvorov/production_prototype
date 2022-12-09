import abc
from abc import ABC
from Production.CalculationMethods import *
from goal_function import goalFunction

class Production(ABC):
    def __init__(self,
                 domain_model,
                 ):
        self.domain_model = domain_model

    @abc.abstractmethod
    def result(self):
        pass


class ProductionOnValueBalancer(Production):
    def __init__(self,
                 case: int,
                 input_params: dict,
                 optimizer,
                 domain_model,
                 ):
        self.case = case
        self.input_params = input_params
        self.optimizer = optimizer
        self.domain_model = domain_model

    def result(self):
        pass

    def _create_parameters(self):
        pass

    def _optimize(self):
        pass


class OilProduction(Production):
    def __init__(self,
                 domain_model,
                 method):