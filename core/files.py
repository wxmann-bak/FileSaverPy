import os
import urllib

__author__ = 'tangz'

from datetime import datetime as dt


DATEFORMAT = '%Y%m%d_%H%M%S'


def gettimestamp(datetime=None, frmt=DATEFORMAT):
    if datetime is None:
        datetime = dt.utcnow()
    return datetime.strftime(frmt)


def buildfilename(base=None, prependval=None, appendval=None, joiner='_'):
    parts = []
    if prependval is not None:
        parts.append(prependval)
    if base is not None:
        parts.append(base)
    if appendval is not None:
        parts.append(appendval)
    return None if not parts else joiner.join(parts)


def withdotsep(extstr):
    return extstr if extstr.startswith('.') else '.' + extstr


def withslash(folder, fwd=True):
    if folder.endswith('/') or folder.endswith('\\'):
        return folder
    else:
        return folder + ('/' if fwd else '\\')


def isfile(url):
    urlcomponents = urllib.parse.urlparse(url)
    basepath = os.path.basename(urlcomponents.path)
    splitbasepath = os.path.splitext(basepath)
    return bool(splitbasepath[1])


def isurl(potential_url):
    return bool(urllib.parse.urlparse(potential_url).scheme)


def geturl(scheme, host, path):
    return urllib.parse.urljoin(scheme + "://" + withslash(host), path)


def get_file_url(parentpath, file):
    return urllib.parse.urljoin(withslash(parentpath), file)


def get_scheme(url):
    return urllib.parse.urlparse(url).scheme


def get_host(url):
    return urllib.parse.urlparse(url).netloc
