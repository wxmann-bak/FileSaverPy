import unittest
import saver

__author__ = 'tangz'

class SaverTests(unittest.TestCase):

    def test_get_http(self):
        url = 'http://www.weather.gov/'
        x = saver.gethtmlforpage(url)
        print(x)
