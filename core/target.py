from datetime import datetime

import functools

from core.model import FileTarget



# class TargetSetting(object):
#     def __init__(self, filename_builder):
#         self.filename_builder = filename_builder
#         self.directory = None
#
#     def _check_set_directory(self):
#         if self.directory is None:
#             raise ValueError("Directory must be set!")
#
#     def fordirectory(self, directory):
#         self.directory = directory
#         return self
#
#     def filetargfromsrc(self, urlsrc):
#         self._check_set_directory()
#         timestamp = datetime.utcnow() if urlsrc.timestamp is None else urlsrc.timestamp
#         newfilename = self.filename_builder(urlsrc.filebase, timestamp)
#         return FileTarget(self.directory, file=newfilename, ext=urlsrc.ext, timestamp=timestamp)
#
#     def filetargfromtemplate(self, template, ext, timestamp=None):
#         self._check_set_directory()
#         file_timestamp = datetime.utcnow() if timestamp is None else timestamp
#         newfilename = self.filename_builder(template, file_timestamp)
#         return FileTarget(self.directory, file=newfilename, ext=ext, timestamp=file_timestamp)


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