import threading
import time
from savers import common
from core import files, timing

__author__ = 'tangz'


class PeriodicSaver(object):
    def __init__(self):
        self.jobs = []

    def addjob(self, onlineurl, saveloc, save_period, mutator=None, timeextractor=None, img_dt=None):
        dirtarg = files.DirectoryTarget(saveloc)
        urlsrc = files.URLSource(onlineurl, timeextractor=timeextractor)
        self.jobs.append(SaveJob(save_period, urlsrc, dirtarg, mutator, img_dt))

    def adddynamicjob(self, onlineurl, saveloc, save_period, mutator=None, timeextractor=None, img_dt=None):
        dirtarg = files.DirectoryTarget(saveloc)
        urlsrc = files.DynamicURLSource(onlineurl, timeextractor=timeextractor)
        self.jobs.append(DynamicSaveJob(save_period, urlsrc, dirtarg, mutator, img_dt))

    def executesaves(self):
        for job in self.jobs:
            job.start()


class SaveJob(threading.Thread):
    def __init__(self, save_period, urlsrc, dirtarg, mutator, img_dt):
        threading.Thread.__init__(self)
        self.urlsrc = urlsrc
        self.dirtarg = dirtarg
        self.mutator = mutator
        self.save_period = save_period
        self.img_dt = img_dt
        self.hist = []

    def run_save(self):
        if timing.passestime(self.urlsrc, timing.TimeConfig(interval=self.img_dt), self.hist):
            targloc = self.dirtarg.get_timestamped_file(self.urlsrc.filebase, self.urlsrc.ext,
                                                        self.urlsrc.timestamp, self.mutator)
            common.dosave(self.urlsrc.url, str(targloc))
            self.hist.append(targloc)

    def run(self):
        while True:
            self.run_save()
            time.sleep(self.save_period.seconds)


class DynamicSaveJob(SaveJob):
    def run_save(self):
        self.urlsrc.refresh()
        SaveJob.run_save(self)