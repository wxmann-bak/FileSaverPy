import unittest

from saverpy import webutil


class WebUtilTests(unittest.TestCase):

    def test_check_if_url_refers_to_file(self):
        not_a_file = 'http://www.google.com'
        a_file = 'http://google.com/index.html'
        self.assertFalse(webutil.isfile(not_a_file))
        self.assertTrue(webutil.isfile(a_file))