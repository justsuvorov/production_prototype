import unittest
from pathlib import Path
from Program.DOTests.WellDoFromSetOfWellsTest import *


class TestDomainModelFromSetOfWells(unittest.TestCase):

    def setUp(self):
        self.domain_model = domain_model(file_path=Path(r'C:\Users\User\Documents\production_prototype\src\Program\data\UnitTestData'))

    def test_objects_count(self):
        self.assertEqual(len(self.domain_model[0]), 1939)
        self.assertEqual(len(self.domain_model[1]), 12)
        self.assertEqual(len(self.domain_model[2]), 4)

    def test_objects_names(self):
        self.assertEqual(self.domain_model[0][0].name[0], '1002')
        self.assertEqual(self.domain_model[0][-1].name[0], '6246')

        self.assertEqual(self.domain_model[1][0].name[0], 'ДНС-1 Арчинского')
        self.assertEqual(self.domain_model[1][-1].name[0], 'ЦППН-1')

        self.assertEqual(self.domain_model[2][0].name[0], 'Арчинское')
        self.assertEqual(self.domain_model[2][-1].name[0], 'Вынгапуровское')

    def test_objects_links(self):
        self.assertEqual(self.domain_model[0][0].link['Fields'][0].name[0], 'Арчинское')
        self.assertEqual(self.domain_model[0][-1].link['Fields'][0].name[0], 'Вынгапуровское')

        self.assertEqual(self.domain_model[0][0].link['Clusters'][0].name[0], 'ДНС-1 Арчинского')
        self.assertEqual(self.domain_model[0][-1].link['Clusters'][0].name[0], 'ДНС-1 Вынгапуровского')

    def test_activity(self):
        self.assertTrue(self.domain_model[0][0].object_info.object_activity)
        self.assertTrue(not self.domain_model[0][-1].object_info.object_activity)