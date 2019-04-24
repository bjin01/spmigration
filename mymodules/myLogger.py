import logging
import sys

def setup_custom_logger(name, level):
    formatter = logging.Formatter(fmt='### %(asctime)s - %(levelname)s - %(module)s - %(message)s')
    formatter = logging.Formatter(fmt='### %(asctime)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter(fmt='### %(levelname)s - %(message)s')

    #handler = logging.StreamHandler()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)

    if level == 0:
       logger.setLevel(logging.ERROR)
    elif level == 1:
       logger.setLevel(logging.INFO)
    elif level >= 2:
       logger.setLevel(logging.DEBUG)

    logger.addHandler(handler)

    return logger
