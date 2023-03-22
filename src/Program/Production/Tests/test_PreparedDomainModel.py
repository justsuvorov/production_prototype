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
import datetime as dt
import unittest


class PreparedDomainModelTest(unittest.TestCase):
    def setUp(self):
        self.domain_model = PreparedDomainModel(domain_model=domain_model(file_path=Path(r'C:\Users\User\Documents\production_prototype\src\Program\data\UnitTestData')),
                                                time_parameters=TimeParameters(
                                                    current_date=dt.date(year=2023, month=3, day=1),
                                                    time_step='Day'),
                                                find_gap=True,
                                                filter={'company': ['Восток'], 'field': ['Арчинское']},
                                                )

    def test_instances(self):
        domain_model, time_parameters = self.domain_model.recalculate_indicators()
        self.assertIsInstance(domain_model, dict)
        self.assertIsInstance(time_parameters, dict)

    def test_filter(self):
        domain_model, time_parameters = self.domain_model.recalculate_indicators()
        self.assertEqual(len(domain_model['Wells']), 73)
        self.assertEqual(len(domain_model['Clusters']), 1)
        self.assertEqual(len(domain_model['Fields']), 1)

    def test_indicators(self):
        domain_model, time_parameters = self.domain_model.recalculate_indicators()
        self.assertEqual(len(domain_model['Wells'][0].indicators['Добыча нефти, тыс. т']), 1797)
        self.assertEqual(len(domain_model['Wells'][0].indicators['FCF']), 1766)
        self.assertEqual(len(domain_model['Wells'][0].indicators['Добыча жидкости, тыс. т']), 1797)

    def test_time_parameters(self):
        domain_model, time_parameters = self.domain_model.recalculate_indicators()
        self.assertEqual(time_parameters['date1'], 0)
        self.assertEqual(time_parameters['date2'], 364)
        self.assertEqual(time_parameters['steps_count'], 366)
        self.assertEqual(time_parameters['current_date'], 28)