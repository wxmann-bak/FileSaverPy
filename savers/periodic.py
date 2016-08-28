import threading
import time
from savers import common
from util import files

__author__ = 'tangz'

class PeriodicSaver(object):
    def __init__(self):
        self.jobs = []

    def addjob(self, onlineurl, saveloc, interval, mutator=None):
        dirtarg = files.DirectoryTarget(saveloc)
        urlsrc = files.URLSource(onlineurl)
        self.jobs.append(SaveJob(interval, urlsrc, dirtarg, mutator))

    def adddynamicjob(self, onlineurl, saveloc, interval, mutator=None):
        dirtarg = files.DirectoryTarget(saveloc)
        urlsrc = files.DynamicURLSource(onlineurl)
        self.jobs.append(DynamicSaveJob(interval, urlsrc, dirtarg, mutator))

    def executesaves(self):
        for job in self.jobs:
            job.start()


class SaveJob(threading.Thread):
    def __init__(self, interval, urlsrc, dirtarg, mutator):
        threading.Thread.__init__(self)
        self.urlsrc = urlsrc
        self.dirtarg = dirtarg
        self.mutator = mutator
        self.interval = interval

    def run_save(self):
        targloc = self.dirtarg.get_timestamped_file(self.urlsrc.filebase, self.urlsrc.ext, self.mutator)
        common.dosave(self.urlsrc.url, str(targloc))

    def run(self):
        while True:
            self.run_save()
            time.sleep(self.interval.seconds)


class DynamicSaveJob(SaveJob):
    def run_save(self):
        self.urlsrc.refresh()
        SaveJob.run_save(self)