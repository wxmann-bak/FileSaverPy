import unittest
from datetime import datetime

from saverpy import objects
from saverpy import predicates
from saverpy.filters import with_predicates


class FiltersTests(unittest.TestCase):
    def setUp(self):
        self.src1 = objects.source(url='http://google.com/img-1.jpg',
                                   timestamp=datetime(2017, 1, 5, 12, 15),
                                   ext='jpg',
                                   filename='img-1')

        self.src2 = objects.source(url='http://google.com/img-2.jpg',
                                   timestamp=datetime(2017, 1, 5, 13, 15),
                                   ext='jpg',
                                   filename='img-2')

        self.src3 = objects.source(url='http://google.com/img-3.gif',
                                   timestamp=datetime(2017, 1, 5, 12, 15),
                                   ext='gif',
                                   filename='img-3')

        self.srcs = [self.src1, self.src2, self.src3]

    def test_should_filter_based_on_predicates(self):
        compfilter = with_predicates(predicates.time_in_range(max_time=datetime(2017, 1, 5, 13, 0)),
                                     predicates.valid_exts('jpg'))

        self.assertEqual(compfilter(self.srcs), [self.src1])
