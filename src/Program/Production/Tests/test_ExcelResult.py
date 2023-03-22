import unittest
from Program.DOTests.WellDoFromSetOfWellsTest import *
from Program.Production.InputParameters import *
from Program.Production.GoalFunction import GoalFunction
from Program.Production.GuiInputInterface import ExcelInterface
from Program.Production.Optimizator import GreedyOptimizer
from Program.Production.Production import OperationalProductionBalancer, CompensatoryProductionBalancer
from Program.Production.ap_parameters import APParameters
from Program.Production.ExcelResult import ExcelResult, ExcelResultPotential, QlikExcelResult
from pathlib import Path
from Program.Production.PreparedDomainModel import PreparedDomainModel
import pandas as pd

class ExcelResultPotentialTest(unittest.TestCase):
    def setUp(self) -> None:
        time_parameters = TimeParameters(
                                            date_start=dt.date(year=2023, month=2, day=1),
                                            current_date=dt.date(year=2023, month=2, day=1),
                                            time_step='Day',
                                            date_end=dt.date(year=2024, month=2, day=1))
        production = CompensatoryProductionBalancer(
                                                        prepared_domain_model=PreparedDomainModel(domain_model=domain_model(file_path=Path(r'C:\Users\User\Documents\production_prototype\src\Program\data\UnitTestData')),
                                                                                                  time_parameters=time_parameters,
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
                                                            goal_function=GoalFunction(parameters=ParametersOfAlgorithm()),
                                                                                    ),
                                                        iterations_count=200,
                                                        )
        production.vbd_index = 70
        self.excel_result = ExcelResultPotential(
                            domain_model=PreparedDomainModel(domain_model=domain_model(file_path=Path(r'C:\Users\User\Documents\production_prototype\src\Program\data\UnitTestData')),
                                                             time_parameters=time_parameters,
                                                             find_gap=False,
                                                             filter={'company': ['Восток'], 'field': ['Арчинское']},
                                                             path=Path(
                                                                 r'C:\Users\User\Documents\production_prototype\src\Program\data\UnitTestData'),

                                                             ).recalculate_indicators()[0]['Wells'],
                            production=production,
                            results='Only sum',
                            dates=time_parameters,
                            )

    def test_dataframe(self):
        dataframe = self.excel_result.dataframe()
        self.assertIsInstance(dataframe, list)
        self.assertIsNotNone(dataframe[0])
        self.assertIsNotNone(dataframe[1])
        self.assertIsNotNone(dataframe[2])
        self.assertIsNotNone(dataframe[3])
        self.assertIsNotNone(dataframe[4])
        self.assertIsNotNone(dataframe[5])

        self.assertEqual(dataframe[0].shape, (70, 366))
        self.assertEqual(dataframe[1].shape, (3, 366))
        self.assertEqual(dataframe[2].shape, (70, 366))
        self.assertEqual(dataframe[3].shape, (3, 366))
        self.assertEqual(dataframe[4].shape, (70, 366))
        self.assertEqual(dataframe[5].shape, (3, 366))