import logging

__author__ = 'tangz'

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler()
ch.setFormatter(format)
logger.addHandler(ch)