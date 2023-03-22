import unittest

from Program.DOTests.WellDoFromSetOfWellsTest import *
from Program.Production.GoalFunction import GoalFunction
from Program.Production.InputParameters import *
from Program.Production.CalculationMethods import SimpleOperations
from Program.Production.Optimizator import GreedyOptimizer
from Program.Production.Production import OperationalProductionBalancer, CompensatoryProductionBalancer
from Program.Production.ap_parameters import APParameters
from Program.Production.ExcelResult import ExcelResult, ExcelResultPotential, QlikExcelResult
from pathlib import Path
from Program.Production.PreparedDomainModel import PreparedDomainModel


class CalculationTest(unittest.TestCase):

    def setUp(self) -> None:

        self.domain_model = domain_model(file_path=Path(
                    r'C:\Users\User\Documents\production_prototype\src\Program\data\UnitTestData'))[0]

    def test_value_on_first_date(self):
        value = SimpleOperations(case=1,
                                 domain_model=self.domain_model,
                                 indicator_name='FCF').calculate()
        self.assertAlmostEqual(value, 56570021, delta=1)                                                                                         ,
        value = SimpleOperations(case=1,
                                 domain_model=self.domain_model,
                                 indicator_name='Добыча нефти, тыс. т').calculate()
        self.assertAlmostEqual(value, 391.2, delta=0.1)
        value = SimpleOperations(case=1,
                                 domain_model=self.domain_model,
                                 indicator_name='Добыча жидкости, тыс. т').calculate()
        self.assertAlmostEqual(value, 5614.7, delta=0.1)

    def test_value_on_date(self):
        value = SimpleOperations(case=1,
                                 date=4,
                                 domain_model=self.domain_model,
                                 indicator_name='FCF').calculate()
        self.assertAlmostEqual(value, 56570021.8, delta=1),
        value = SimpleOperations(case=1,
                                 date=4,
                                 domain_model=self.domain_model,
                                 indicator_name='Добыча нефти, тыс. т').calculate()
        self.assertAlmostEqual(value, 335.9, delta=0.1)
        value = SimpleOperations(case=1,
                                 date=4,
                                 domain_model=self.domain_model,
                                 indicator_name='Добыча жидкости, тыс. т').calculate()
        self.assertAlmostEqual(value, 5553.4, delta=0.1)

    def test_average_value(self):
        value = SimpleOperations(case=2,
                                 domain_model=self.domain_model,
                                 indicator_name='FCF').calculate()
        self.assertAlmostEqual(value, 56570021.8, delta=1
                               ),
        value = SimpleOperations(case=2,
                                 domain_model=self.domain_model,
                                 indicator_name='Добыча нефти, тыс. т').calculate()
        self.assertAlmostEqual(value, 317.9, delta=0.1)
        value = SimpleOperations(case=2,
                                 domain_model=self.domain_model,
                                 indicator_name='Добыча жидкости, тыс. т').calculate()
        self.assertAlmostEqual(value, 5530.85, delta=0.1)

    def test_average_value(self):
        value = SimpleOperations(case=3,
                                 domain_model=self.domain_model,
                                 indicator_name='FCF').calculate()
        self.assertAlmostEqual(value, 56570021.8, delta=1
                               ),
        value = SimpleOperations(case=3,
                                 domain_model=self.domain_model,
                                 indicator_name='Добыча нефти, тыс. т').calculate()
        self.assertAlmostEqual(sum(value), 3874.1, delta=0.1)
        value = SimpleOperations(case=3,
                                 domain_model=self.domain_model,
                                 indicator_name='Добыча жидкости, тыс. т').calculate()
        self.assertAlmostEqual(sum(value), 66441.87, delta=0.1)

    def test_cumulative_value(self):
        value = SimpleOperations(case=4,
                                 domain_model=self.domain_model,
                                 indicator_name='FCF').calculate()
        self.assertAlmostEqual(value, 20993171.8, delta=1
                               ),
        value = SimpleOperations(case=4,
                                 domain_model=self.domain_model,
                                 indicator_name='Добыча нефти, тыс. т').calculate()
        self.assertAlmostEqual(value, 3544.86, delta=0.1)
        value = SimpleOperations(case=4,
                                 domain_model=self.domain_model,
                                 indicator_name='Добыча жидкости, тыс. т').calculate()
        self.assertAlmostEqual(value, 60899.78, delta=0.1)