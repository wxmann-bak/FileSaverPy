import unittest
from datetime import datetime

from saverpy import objects
from saverpy import predicates


class PredicatesTests(unittest.TestCase):
    def setUp(self):
        self.timestamp = datetime(2017, 1, 5, 12, 15)
        self.ext = 'jpg'
        self.imgname = 'img-1'
        self.src = objects.source(url='http://blah.com/img-1.jpg',
                                  timestamp=self.timestamp,
                                  ext=self.ext,
                                  filename=self.imgname)

    def test_ext_predicate(self):
        self.assertTrue(predicates.valid_exts('jpg', 'png')(self.src))
        self.assertFalse(predicates.valid_exts('gif', 'png')(self.src))

    def test_ext_predicate_with_periods_in_args(self):
        self.assertTrue(predicates.valid_exts('.jpg', '.png')(self.src))
        self.assertFalse(predicates.valid_exts('.gif', '.png')(self.src))

    def test_ext_predicate_case_insensitivity(self):
        self.assertTrue(predicates.valid_exts('.JPG', '.PNG')(self.src))
        self.assertFalse(predicates.valid_exts('.GIF', '.PNG')(self.src))

    def test_min_divisible_predicate(self):
        self.assertTrue(predicates.min_divisible_by(15)(self.src))
        self.assertFalse(predicates.min_divisible_by(10)(self.src))

    def test_time_range_predicate_both_endpoints_inclusive(self):
        self.assertTrue(predicates.time_in_range(datetime(2017, 1, 5, 12, 15), datetime(2017, 1, 5, 12, 15))(self.src))
        self.assertTrue(predicates.time_in_range(datetime(2017, 1, 5, 12, 0), datetime(2017, 1, 5, 12, 30))(self.src))
        self.assertFalse(predicates.time_in_range(datetime(2017, 1, 5, 12, 16), datetime(2017, 1, 5, 12, 30))(self.src))

    def test_time_range_predicate_both_endpoints_exclusive(self):
        self.assertFalse(
            predicates.time_in_range(datetime(2017, 1, 5, 12, 15), datetime(2017, 1, 5, 12, 20), False)(self.src))
        self.assertTrue(predicates.time_in_range(datetime(2017, 1, 5, 12, 0), datetime(2017, 1, 5, 12, 30))(self.src))

    def test_time_range_predicate_only_min_time(self):
        self.assertTrue(predicates.time_in_range(min_time=datetime(2017, 1, 5, 12, 15), inclusive=True)(self.src))
        self.assertFalse(predicates.time_in_range(min_time=datetime(2017, 1, 5, 12, 15), inclusive=False)(self.src))

        self.assertTrue(predicates.time_in_range(min_time=datetime(2017, 1, 5, 12, 0))(self.src))
        self.assertFalse(predicates.time_in_range(min_time=datetime(2017, 1, 5, 13, 0))(self.src))

    def test_time_range_predicate_only_max_time(self):
        self.assertTrue(predicates.time_in_range(max_time=datetime(2017, 1, 5, 12, 15), inclusive=True)(self.src))
        self.assertFalse(predicates.time_in_range(max_time=datetime(2017, 1, 5, 12, 15), inclusive=False)(self.src))

        self.assertTrue(predicates.time_in_range(max_time=datetime(2017, 1, 5, 13, 0))(self.src))
        self.assertFalse(predicates.time_in_range(max_time=datetime(2017, 1, 5, 12, 0))(self.src))

    def test_name_contains_predicate(self):
        self.assertTrue(predicates.name_contains('1')(self.src))
        self.assertFalse(predicates.name_contains('2')(self.src))
