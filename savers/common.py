import os
import urllib.request

from core.logs import logger

__author__ = 'tangz'


def dosave(srcfile, destloc):
    if os.path.isfile(destloc):
        raise SaveError("File: {0} already exists, cannot save it".format(destloc))
    logger.info("Saving file from {0} to {1}".format(srcfile, destloc))
    urllib.request.urlretrieve(srcfile, destloc)


class SaveError(Exception):
    pass
