from pathlib import Path
import datetime
import unittest
import string
import random

from data_manipulator import DataManipulator
import data_manipulator


class TestDataManipulation(unittest.TestCase):
    def setUp(self):
        self.manipulator = DataManipulator(Path('test_data.json'))

    def test_process_data(self):
        # Test string manipulation
        self.manipulator.process_dict_data()
        self.assertEqual(self.manipulator.processed_data['name'], 'leinaD')
        self.assertEqual(self.manipulator.processed_data['city'], 'vivA leT')

        # Test list duplication
        self.assertEqual(self.manipulator.processed_data['fruits'], ['apple', 'orange', 'banana'])

        # Test datetime year change
        self.assertEqual(self.manipulator.processed_data['start_time'], '2021/12/31 23:59:59')
        self.assertEqual(self.manipulator.processed_data['end_time'], '2021/01/01 00:00:00')

    def test_verify_path(self):
        # Negative
        # empty/None path
        self.assertFalse(DataManipulator.verify_path(Path('')))
        self.assertFalse(DataManipulator.verify_path(None))

        # Positive
        # not exist path
        self.assertFalse(DataManipulator.verify_path(Path('not/exist/path')))
        # folder path
        self.assertFalse(DataManipulator.verify_path(Path().resolve()))
        # current file path
        self.assertTrue(DataManipulator.verify_path(Path(__file__)))

    def test_manipulate_date(self):
        # Negative
        self.assertIsNone(DataManipulator.manipulate_date(None))
        # Positive
        # current date path
        date_format = data_manipulator.VALID_DATE_FORMAT
        now = datetime.datetime.now()
        now_manip_str = now.replace(year=2021).strftime(date_format)
        self.assertEqual(DataManipulator.manipulate_date(now), now_manip_str)

    def test_manipulate_string(self):
        # Negative
        # None string
        self.assertIsNone(DataManipulator.manipulate_string(None))
        # Positive
        # string with whitespaces
        test_str_1 = ' abc '
        manip_str_1 = 'cba'
        self.assertEqual(DataManipulator.manipulate_string(test_str_1), manip_str_1)

        # Random string
        test_str_2 = ''.join(
            random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits + ' ', k=30))
        reversed_str_2 = test_str_2.strip()[::-1]
        self.assertEqual(DataManipulator.manipulate_string(test_str_2), reversed_str_2)

    def test_manipulate_list(self):
        # Negative
        # Empty / None list
        self.assertIsNone(DataManipulator.manipulate_list([]))
        self.assertIsNone(DataManipulator.manipulate_list(None))
        # Positive
        # list with duplicates ints
        self.assertEqual(DataManipulator.manipulate_list([1, 2, 3, 1, 2, 3]), [1, 2, 3])
        # list with duplicates floats
        self.assertEqual(DataManipulator.manipulate_list([1.2, 2.3, 3.5, 1.2, 2.3, 3.4]), [1.2, 2.3, 3.5, 3.4])
        # list with duplicates strs
        self.assertEqual(DataManipulator.manipulate_list(['a', 'b', 'a']), ['a', 'b'])
        # list with duplicates dicts
        self.assertEqual(DataManipulator.manipulate_list([{'a': 'aa', 'b': 'bb'}, {'a': 'aa', 'b': 'bb'}]),
                         [{'a': 'aa', 'b': 'bb'}])
