import unittest

from Program.DOTests.WellDoFromSetOfWellsTest import *
from Program.Production.GoalFunction import GoalFunction
from Program.Production.InputParameters import *

from Program.Production.Optimizator import GreedyOptimizer
from Program.Production.Production import OperationalProductionBalancer, CompensatoryProductionBalancer
from Program.Production.ap_parameters import APParameters
from Program.Production.ExcelResult import ExcelResult, ExcelResultPotential, QlikExcelResult
from pathlib import Path
from Program.Production.PreparedDomainModel import PreparedDomainModel
import pickle


class ProductionBalancerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.balancer = CompensatoryProductionBalancer(
                                                        prepared_domain_model=PreparedDomainModel(domain_model=domain_model(file_path=Path(r'C:\Users\User\Documents\production_prototype\src\Program\data\UnitTestData')),
                                                                                                  time_parameters=TimeParameters(
                                                                                                  date_start=dt.date(year=2023, month=2, day=1),
                                                                                                  current_date=dt.date(year=2023, month=2, day=1),
                                                                                                  time_step='Day',
                                                                                                  date_end=dt.date(year=2024, month=2, day=1)),
                                                                                                  find_gap=False,
                                                                                                  filter={'company': ['Восток'], 'field': ['Арчинское']},
                                                                                                  path=Path(r'C:\Users\User\Documents\production_prototype\src\Program\data\UnitTestData'),

                                                                                                  ),
                                                        input_parameters=ParametersOfAlgorithm(),
                                                        optimizator=GreedyOptimizer(
                                                            constraints=ParametersOfAlgorithm(),
                                                            parameters=APParameters(inKeys=['ObjectActivity'],
                                                                                    outKeys=['Добыча нефти, тыс. т', 'FCF'],
                                                                                    inValues=[[]]
                                                                                    ),
                                                            goal_function=GoalFunction(
                                                                parameters=ParametersOfAlgorithm(),
                                                                                      ),
                                                                                    ),
                                                        iterations_count=200,
                                                        )

    def test_balancer_result(self):
        result = self.balancer.result(path=Path(r'C:\Users\User\Documents\production_prototype\src\Program\data\UnitTestData')),

        self.assertEqual(self.balancer.vbd_index, 70) #проверка на количество вбд скважин
        self.assertEqual(len(self.balancer.turn_off_nrf_wells), 5) #проверка алгоритма отключения НРФ
        self.assertEqual(self.balancer.optimizer.best_kid[0][-1], 61) #проверка постановки бригад
        self.assertEqual(self.balancer.optimizer.best_kid[0][-2], 31) #проверка постановки бригад
        self.assertEqual(self.balancer.optimizer.best_kid[0][-3], 31) #проверка постановки бригад
        self.assertEqual(len(list(filter(None, self.balancer.result_dates))), 3)#количество скважин ВБД

        self.assertIsInstance(result[0], dict)
        self.assertEqual(len(result[0]['Wells']), 73)
        self.assertEqual(len(result[0]['Clusters']), 1)
        self.assertEqual(len(result[0]['Fields']), 1)


