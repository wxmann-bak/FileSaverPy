from datetime import datetime, timedelta
import unittest
from unittest.mock import MagicMock, patch

from core import saver


__author__ = 'tangz'


class ContextTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://cool.html/img.jpg'
        self.directory = 'C://Self/Pictures'
        self.srcsetting = MagicMock()
        self.targsetting = MagicMock()

    @patch('core.saver._SaveJob')
    def test_should_submit_and_retrieve_job(self, savejob):
        context = saver.Context(self.srcsetting, self.targsetting)
        jobid = 'a'
        submitted_job = context.submit(jobid, self.url, self.directory)
        self.assertEqual(context.getjob(jobid), submitted_job)

    def test_should_raise_error_if_submit_same_jobid_twice(self):
        context = saver.Context(self.srcsetting, self.targsetting)
        jobid = 'a'
        context.submit(jobid, self.url, self.directory)
        with self.assertRaises(ValueError):
            context.submit(jobid, self.url, self.directory)

    @patch('core.saver._SaveJob')
    def test_should_create_job_when_submit_jobid(self, savejob):
        context = saver.Context(self.srcsetting, self.targsetting)
        jobid = 'a'
        context.submit(jobid, self.url, self.directory)
        savejob.assert_called_with(jobid, context, self.url, self.directory)

    def test_should_call_job_start_when_job_is_run(self):
        context = saver.Context(self.srcsetting, self.targsetting)
        thejob = MagicMock()
        thejob.start = MagicMock()
        jobid = 'a'
        with patch.object(context, 'getjob', return_value=thejob, autospec=True) as mock_get_job:
            context.runjob(jobid)
            mock_get_job.assert_called_with(jobid)
            thejob.start.assert_called_with()

    def test_should_call_job_stop_when_job_is_stopped(self):
        context = saver.Context(self.srcsetting, self.targsetting)
        thejob = MagicMock()
        thejob.stop = MagicMock()
        jobid = 'a'
        with patch.dict(context._jobs, {jobid: thejob}):
            context.stop(jobid)
            thejob.stop.assert_called_with()

    @patch('core.timing.current_time')
    def test_should_start_job_with_delay(self, right_now):
        dummydate = datetime(year=1991, month=1, day=1)
        right_now.return_value = dummydate
        number_of_seconds = 5
        timing_delta = timedelta(seconds=number_of_seconds)
        begin = dummydate + timing_delta

        context = saver.Context(self.srcsetting, self.targsetting)
        thejob = MagicMock()
        jobid = 'a'
        with patch.object(context, 'getjob', return_value=thejob, autospec=True) as mock_get_job, patch(
                'threading.Timer') as mock_timer:
            mock_timer.return_value.start = MagicMock()
            mock_start = mock_timer.return_value.start

            context.runjob(jobid, begin=begin)
            mock_get_job.assert_called_with(jobid)
            mock_timer.assert_called_with(number_of_seconds, thejob.start)
            mock_start.assert_called_with()

    @patch('core.timing.current_time')
    def test_should_schedule_end_job(self, right_now):
        dummydate = datetime(year=1991, month=1, day=1)
        right_now.return_value = dummydate
        number_of_seconds = 10
        timing_delta = timedelta(seconds=number_of_seconds)
        ending = dummydate + timing_delta

        context = saver.Context(self.srcsetting, self.targsetting)
        thejob = MagicMock()
        jobid = 'a'
        with patch.object(context, 'getjob', return_value=thejob, autospec=True) as mock_get_job, patch(
                'threading.Timer') as mock_timer:
            mock_timer.return_value.start = MagicMock()
            mock_start = mock_timer.return_value.start

            context.runjob(jobid, end=ending)
            mock_get_job.assert_called_with(jobid)
            mock_timer.assert_called_with(number_of_seconds, thejob.stop)
            mock_start.assert_called_with()