import logging

def get_logger(level=None):
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('BenderBot')
    if level:
        logger.setLevel(getattr(logging, level))
    return logger
