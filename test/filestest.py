import os
import unittest

import core.model
from core import files

__author__ = 'tangz'


class FilesTests(unittest.TestCase):

    def test_should_add_slash(self):
        testdirs = ['C:/Me', 'http://Me', 'C:/Me/','http://Me/']
        results = ['C:/Me/', 'http://Me/', 'C:/Me/', 'http://Me/']
        for i in range(len(testdirs)):
            self.assertEqual(files.withslash(testdirs[i]), results[i])

    def test_should_add_dot(self):
        testext = ['.jpg', 'JPG', 'jpg']
        results = ['.jpg', '.JPG', '.jpg']
        for i in range(len(testext)):
            self.assertEqual(files.withdotsep(testext[i]), results[i])

    def test_create_url_src(self):
        url = 'http://weather.rap.ucar.edu/radar/nws_nids/BREF1/KDLH/20160511_085022_gray.png'
        src = core.model.URLSource(url)
        self.assertEqual(src.url, url)
        self.assertEqual(src.filebase, '20160511_085022_gray')
        self.assertEqual(src.ext, 'png')
        self.assertEqual(src.host, 'weather.rap.ucar.edu')
        self.assertEqual(src.scheme, 'http')

    def test_file_target(self):
        dir = "C:\Me"
        targ = core.model.FileTarget("C:\Me", "abc", "jpg", None)
        self.assertEqual(str(targ), os.path.join(dir, "abc.jpg"))

    def test_file_target_with_dot_in_ext(self):
        dir = "C:\Me"
        targ = core.model.FileTarget("C:\Me", "abc", ".jpg", None)
        self.assertEqual(str(targ), os.path.join(dir, "abc.jpg"))

    def test_should_confirm_is_url(self):
        correcturl = "http://weather.rap.ucar.edu/radar/nws_nids/BREF1/KDLH/20160511_085022_gray.png"
        notcorrecturl = "weather.rap.ucar.edu"
        self.assertTrue(files.isurl(correcturl))
        self.assertFalse(files.isurl(notcorrecturl))

    def test_should_confirm_is_file(self):
        correctfile = "http://weather.rap.ucar.edu/radar/nws_nids/BREF1/KDLH/20160511_085022_gray.png"
        notcorrectfile = "weather.rap.ucar.edu/radar"
        self.assertTrue(files.isfile(correctfile))
        self.assertFalse(files.isfile(notcorrectfile))

    def test_should_get_url_from_scheme_host_path(self):
        scheme = 'http'
        host = 'weather.rap.ucar.edu'
        path = '/radar/nws_nids/BREF1/KDLH/20160511_085022_gray.png'
        expected_url = 'http://weather.rap.ucar.edu/radar/nws_nids/BREF1/KDLH/20160511_085022_gray.png'
        self.assertEqual(files.geturl(scheme, host, path), expected_url)

    def test_should_get_file_url_from_path_and_file(self):
        parentpath = 'http://weather.rap.ucar.edu/radar/nws_nids/BREF1/KDLH'
        file = '20160511_085022_gray.png'
        expected_url = 'http://weather.rap.ucar.edu/radar/nws_nids/BREF1/KDLH/20160511_085022_gray.png'
        self.assertEqual(files.get_file_url(parentpath, file), expected_url)