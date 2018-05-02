from settings import SETTINGS as settings
import logging
import sys


def get_pretty_logger(name):
    """create a useful logger"""
    logger = logging.Logger(name)
    filename = settings.get("LOGFILE", "/tmp/antifraud.log")
    logLevel = settings.get("LOGLEVEL", 6)
    logger.setLevel(logLevel)
    LOG_FORMAT = u'%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s'
    formatter = logging.Formatter(LOG_FORMAT)
    filehandler = logging.FileHandler(filename)
    console = logging.StreamHandler(sys.stdout)
    filehandler.setFormatter(formatter)
    console.setFormatter(formatter)
    logger.addHandler(filehandler)
    logger.addHandler(console)
    return logger
