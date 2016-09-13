import os
import threading
import time
import urllib.request

from core.logs import logger


class SaveError(Exception):
    pass


def dosave(srcfile, destloc):
    if os.path.isfile(destloc):
        logger.warn("File: {0} already exists, cannot save it".format(destloc))
        return False
    else:
        logger.info("Saving file from {0} to {1}".format(srcfile, destloc))
        urllib.request.urlretrieve(srcfile, destloc)
        return True


class Saver(object):
    def __init__(self, srcsetting, targsetting, saveperiod=None, min_img_interval=None):
        self.srcsetting = srcsetting
        self.targsetting = targsetting
        self.saveperiod = saveperiod
        self.min_img_interval = min_img_interval
        self._jobs = {}

    def submit(self, jobid, url, directory):
        if jobid in self._jobs:
            raise ValueError("Job: {0} already exists, try using a different job id".format(jobid))
        self._jobs[jobid] = _SaveJob(self.srcsetting, self.targsetting, self.saveperiod,
                                     self.min_img_interval, url, directory)

    def has_job(self, jobid):
        return jobid in self._jobs

    def get_job(self, jobid):
        return self._jobs.get(jobid, None)

    def clear(self, jobid):
        if jobid in self._jobs:
            del self._jobs[jobid]

    def save(self):
        for jobid in self._jobs:
            self._jobs[jobid].start()


class _SaveJob(object):
    def __init__(self, srcsetting, targsetting, saveperiod, min_img_interval, url, directory):
        self.srcsetting = srcsetting
        self.targsetting = targsetting
        self.saveperiod = saveperiod
        self.min_img_interval = min_img_interval
        self.url = url
        self.directory = directory
        self.hist = []
        self._thread = None
        self._init_thread_if_necessary()

    def _passes_interval(self, urlsrc):
        if not self.hist:
            return True
        elif not urlsrc.timestamp:
            return True
        elif urlsrc.timestamp in [hist_save.timestamp for hist_save in self.hist]:
            logger.warn("image: {0} with time: {1} already exists".format(urlsrc.url, urlsrc.timestamp))
            return False
        elif self.min_img_interval:
            dt = urlsrc.timestamp - self.hist[-1].timestamp
            if dt < self.min_img_interval:
                logger.debug(
                    "timing between images insufficient for: {0} (timestamp: {1})".format(urlsrc.url, urlsrc.timestamp))
                return False
            else:
                return True
        else:
            return True

    def _init_thread_if_necessary(self):
        if self.saveperiod is not None:
            self._thread = _SaveThread(self)

    def start(self):
        if not self._thread:
            self.execute_save()
        else:
            self._thread.start()

    def execute_save(self):
        urlsrcs_to_execute = self.srcsetting.urlsrcs_for(self.url)
        for src in urlsrcs_to_execute:
            if self._passes_interval(src):
                self._actually_save(src)

    def _actually_save(self, urlsrc):
        target = self.targsetting.withdir(self.directory)
        filetarg = target.tofiletarget(urlsrc)
        completed = dosave(urlsrc.url, str(filetarg))
        if completed:
            self.hist.append(filetarg)


class _SaveThread(threading.Thread):
    def __init__(self, job):
        threading.Thread.__init__(self)
        self.job = job

    def run(self):
        while True:
            self.job.execute_save()
            time.sleep(self.job.saveperiod.seconds)
