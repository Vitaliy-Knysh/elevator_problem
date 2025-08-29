import logging
from os import mkdir
from os.path import abspath, isdir


def get_logger() -> logging.Logger:
    if not isdir(log_dir := abspath('../logs/')):
        mkdir(log_dir)
    filename = log_dir + '/elevator_log.log'
    logging.basicConfig(level=logging.INFO, filename=filename, filemode="w")
    return logging.getLogger()
