import unittest

import files


__author__ = 'tangz'

class FileNameTests(unittest.TestCase):

    def test_should_get_filename(self):
        timestamp = files.gettimestamp()
        fileext = '.jpg'
        filename = files.buildfilename(fileext, prependval='OAX', appendval=timestamp)
        self.assertEqual(filename, 'OAX_' + timestamp + fileext)

    def test_should_add_slash(self):
        testdirs = ['C:/Me', 'C:\\Me', 'C:/Me/','C:/Me\\']
        results = ['C:/Me/', 'C:\\Me/', 'C:/Me/', 'C:/Me\\']
        for i in range(len(testdirs)):
            self.assertEqual(files.withslash(testdirs[i]), results[i])

    def test_should_add_dot(self):
        testext = ['.jpg', 'JPG', 'jpg']
        results = ['.jpg', '.JPG', '.jpg']
        for i in range(len(testext)):
            self.assertEqual(files.withdotsep(testext[i]), results[i])

    def test_create_url_src(self):
        url = 'http://weather.rap.ucar.edu/radar/nws_nids/BREF1/KDLH/20160511_085022_gray.png'
        src = files.URLSource(url)
        self.assertEqual(src.url, url)
        self.assertEqual(src.filebase, '20160511_085022_gray')
        self.assertEqual(src.ext, 'png')


