import logging
import os
import threading
import urllib.request

from core import timing
from core.logs import logger


_LOG_TIME_DATEFORMAT = "%Y-%m-%d %H:%M:%S"

class SaveError(Exception):
    pass


def dosave(srcfile, destloc, retry_count=0, retries=3):
    if os.path.isfile(destloc):
        logger.warn("File: {0} already exists, cannot save it".format(destloc))
        return False
    else:
        logger.info("Saving file from {0} to {1}".format(srcfile, destloc))
        try:
            urllib.request.urlretrieve(srcfile, destloc)
            logging.info('File successfully saved.')
            return True
        except:
            count = retry_count
            if retry_count == 0:
                logging.exception('Error occurred while saving:')
            else:
                logging.info('Retry number: {0} failed...'.format(retry_count))
            if count < retries:
                count += 1
                return dosave(srcfile, destloc, retry_count=count, retries=retries)
            logging.info('Giving up!')
            return False


class Context(object):
    def __init__(self, name, srcsetting, targsetting, executor=dosave, saveperiod=None, min_img_interval=None):
        self.name = name
        self.srcsetting = srcsetting
        self.targsetting = targsetting
        self.executor = executor
        self.saveperiod = saveperiod
        self.min_img_interval = min_img_interval
        self._jobs = {}

    def hasjob(self, jobid):
        return jobid in self._jobs

    def getjob(self, jobid):
        if jobid not in self._jobs:
            raise ValueError("Job {0} has not been submitted.".format(jobid))
        return self._jobs[jobid]

    def submit(self, jobid, url, saveloc):
        if jobid in self._jobs:
            raise ValueError("Job {0} already exists".format(jobid))
        thejob = _SaveJob(jobid, self, url, saveloc)
        thejob.name = jobid
        self._jobs[jobid] = thejob
        return thejob

    def runjob(self, jobid, begin=None, end=None):
        thejob = self.getjob(jobid)
        now = timing.current_time()
        if begin and end and begin > end:
            raise ValueError("Begin job at a later time than terminate the job")
        if begin:
            Context._schedule_begin(now, thejob, begin)
        else:
            thejob.start()
        if end:
            Context._schedule_terminate(now, thejob, end)

    def runall(self, begin=None, end=None):
        for jobid in self._jobs:
            self.runjob(jobid, begin, end)

    def stop(self, jobid):
        try:
            thejob = self._jobs[jobid]
            if thejob.is_running():
                thejob.stop()
        except KeyError:
            logger.warn("Could not find job: {0} to stop".format(jobid))

    def stopall(self):
        for jobid in self._jobs:
            self.stop(jobid)

    @staticmethod
    def _schedule_begin(now, job, begin):
        if begin < now:
            raise ValueError("Begin time < right now")
        logger.info('Set job {0} to begin at {1}'.format(job.name, begin.strftime(_LOG_TIME_DATEFORMAT)))
        dt = begin - now
        timer = threading.Timer(dt.seconds, job.start)
        timer.start()

    @staticmethod
    def _schedule_terminate(now, job, end):
        if end < now:
            raise ValueError("End time < right now")
        logger.info('Set job {0} to terminate at {1}'.format(job.name, end.strftime(_LOG_TIME_DATEFORMAT)))
        dt = end - now
        timer = threading.Timer(dt.seconds, job.stop)
        timer.start()

    def __iter__(self):
        return iter(self._jobs.values())


class _SaveJob(threading.Thread):
    def __init__(self, name, context, url, saveloc):
        threading.Thread.__init__(self, name=name)
        self.context = context
        self.url = url
        self.saveloc = saveloc
        self._hist = []
        self._stop_event = threading.Event()

    def _passes_interval(self, urlsrc):
        if not self._hist:
            return True
        elif not urlsrc.timestamp:
            return True
        elif urlsrc.timestamp in [hist_save.timestamp for hist_save in self._hist]:
            logger.warn("image: {0} with time: {1} already exists".format(urlsrc.url, urlsrc.timestamp))
            return False
        elif self.context.min_img_interval:
            dt = urlsrc.timestamp - self._hist[-1].timestamp
            if dt < self.context.min_img_interval:
                logger.debug(
                    "timing between images insufficient for: {0} (timestamp: {1})".format(urlsrc.url, urlsrc.timestamp))
                return False
            else:
                return True
        else:
            return True

    def run(self):
        logger.info('Starting job: ' + self.name)
        if self.context.saveperiod:
            self._save_periodic()
        else:
            self._save_single()

    def stop(self):
        logger.info('Stopping job: ' + self.name)
        self._stop_event.set()

    def is_running(self):
        if self._stop_event.is_set():
            return False
        return True

    def _save_single(self):
        urlsrcs_to_execute = self.context.srcsetting.urlsrcs_for(self.url)
        for src in urlsrcs_to_execute:
            if self._passes_interval(src):
                self._execute_save(src)

    def _save_periodic(self):
        while not self._stop_event.is_set():
            self._save_single()
            self._stop_event.wait(self.context.saveperiod.seconds)

    def _execute_save(self, urlsrc):
        target = self.context.targsetting.withdir(self.saveloc)
        filetarg = target.tofiletarget(urlsrc)
        completed = self.context.executor(urlsrc.url, str(filetarg))
        if completed:
            self._hist.append(filetarg)
