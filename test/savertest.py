import unittest
from unittest.mock import MagicMock, patch
from core import saver

__author__ = 'tangz'


class SaverTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://cool.html/img.jpg'
        self.directory = 'C://Self/Pictures'

    def test_should_submit_and_retrieve_jobid(self):
        srcsetting = MagicMock()
        targsetting = MagicMock()
        thesaver = saver.Saver(srcsetting, targsetting)

        jobid = 'a'
        thesaver.submit(jobid, self.url, self.directory)

        self.assertTrue(thesaver.has_job(jobid))
        self.assertIsNotNone(thesaver.get_job(jobid))

    def test_should_submit_and_clear_job(self):
        srcsetting = MagicMock()
        targsetting = MagicMock()
        thesaver = saver.Saver(srcsetting, targsetting)

        jobid = 'a'
        thesaver.submit(jobid, self.url, self.directory)
        thesaver.clear(jobid)

        self.assertFalse(thesaver.has_job(jobid))
        self.assertIsNone(thesaver.get_job(jobid))

    def test_should_raise_error_if_submit_same_jobid_twice(self):
        srcsetting = MagicMock()
        targsetting = MagicMock()
        thesaver = saver.Saver(srcsetting, targsetting)

        jobid = 'a'
        thesaver.submit(jobid, self.url, self.directory)
        with self.assertRaises(ValueError):
            thesaver.submit(jobid, self.url, self.directory)

    @patch('core.saver._SaveJob')
    def test_should_create_job_when_submit_jobid(self, savejob):
        srcsetting = MagicMock()
        targsetting = MagicMock()
        thesaver = saver.Saver(srcsetting, targsetting)

        jobid = 'a'
        thesaver.submit(jobid, self.url, self.directory)

        savejob.assert_called_with(srcsetting, targsetting, None, None, self.url, self.directory)