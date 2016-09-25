import logging

__author__ = 'tangz'

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
frmt = logging.Formatter("%(asctime)s - %(threadName)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler()
ch.setFormatter(frmt)
logger.addHandler(ch)