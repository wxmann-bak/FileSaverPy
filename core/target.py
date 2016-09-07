import os
from datetime import datetime

import functools

from core.files import withdotsep


def copyfilename(mutator=None):
    return TargetSetting(mutator, overwriting_template=None)


def withfiletemplate(filename_func, template, **kwargs):
    filename_builder = functools.partial(filename_func, **kwargs)
    return TargetSetting(filename_builder, template)


class TargetSetting(object):
    def __init__(self, filename_builder=None, overwriting_template=None):
        self.folder = None
        self.filename_builder = filename_builder
        self.overwriting_template = overwriting_template

    def _check_has_dir(self):
        if not self.folder:
            raise ValueError("Must select directory before outputting any files")

    def withdir(self, directory):
        self.folder = directory
        return self

    def tofiletarget(self, urlsrc):
        self._check_has_dir()
        thetime = urlsrc.timestamp if urlsrc.timestamp else datetime.utcnow()
        if self.overwriting_template:
            file = self.filename_builder(self.overwriting_template, thetime)
        else:
            file = urlsrc.filebase if self.filename_builder is None else self.filename_builder(urlsrc.filebase, thetime)
        return FileTarget(self.folder, file=file, ext=urlsrc.ext, timestamp=thetime)


class FileTarget(object):
    def __init__(self, folder, file, ext, timestamp):
        self.folder = folder
        self.file = file
        self.ext = ext
        self.timestamp = timestamp

    def __str__(self):
        return os.path.join(self.folder, self.file + withdotsep(self.ext))