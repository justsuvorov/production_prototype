import datetime
import os.path

from Program.Production.GuiInputInterface import ExcelInterface
import unittest
from pathlib import Path

class GuiInputInterfaceExcelCase1Test(unittest.TestCase):

    def setUp(self) -> None:
        self.gui = ExcelInterface(filepath=Path(r'C:\Users\User\Documents\production_prototype\src\Program\data\UnitTestData'))

    def test_iterations_count(self):
        pass

    def test_filter(self):
        field_iter = [1, 1, 9, 9]
        company_iter = [1, 7, 1, 7]
        field = [['Арчинское'], ['Арчинское', 'Западно-Лугинецкое', 'Крапивинское', 'Кулгинское', 'Нижнелугинецкое', 'Смоляное', 'Урманское', 'Шингинское', 'Южно-Табаганское'],['Арчинское'],['Арчинское']]
        for i in range(1, 5):
            path = r'C:\Users\User\Documents\production_prototype\src\Program\data\UnitTestData\Interface'
            path3 = str(i)
            path3 = os.path.join(path, path3)
            gui = ExcelInterface(filepath=
                    Path(path3))
            self.assertEqual(gui.company_iterations(), company_iter[i-1])
            self.assertEqual(gui.field_iterations(company_index=0), field_iter[i - 1])
            self.assertEqual(gui.chosen_objects(
                company_index=0,
                field_index=0), {'company': 'Восток', 'field': field[i-1]})

    def test_parameters(self):
        par = self.gui.parameter_of_algorithm()
        time = self.gui.time_parameters()

        self.assertEqual(par.max_objects_per_day,  8)
        self.assertEqual(par.days_per_object, 5)
        self.assertEqual(par.compensation, False)

        self.assertEqual(time.date_start, datetime.date(year=2023, month=2,day=1))
        self.assertEqual(time.date_begin, datetime.date(year=2023, month=2, day=1))


