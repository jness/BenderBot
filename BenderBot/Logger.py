import logging

def get_logger(level=None):
    '''This method will define us a **logger** for BenderBot.
    
    Using the function works like so::
        
        from BenderBot.Logger import get_logger
        logger = get_logger(level='INFO')
        logger.warning('Killing ExternalProcess')
    '''
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('BenderBot')
    if level:
        logger.setLevel(getattr(logging, level))
    return logger
