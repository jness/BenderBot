from BenderBot.Configuration import get_config
from BenderBot.Logger import get_logger
from BenderBot.IRC import IRC

from ConfigParser import NoOptionError, NoSectionError
from multiprocessing import Process
from importlib import import_module
import argparse

def main():
    '''This is the main BenderBot script, it ties all the pieces
    together and runs our active bot'''

    # process args for debug
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action="store_true", dest="debug",
                        default=False, help='Turn on verbose debugging')
    args = parser.parse_args()

    global config, logger    
    config = get_config()
    
    # set logging level based on argparse
    if args.debug:
        logger = get_logger(level='DEBUG')
    else:
        logger = get_logger(level='INFO')
    
    # call our IRC core class to handle everything IRC
    irc = IRC(logger=logger)
    irc.connect()
    
    # find all of our processes
    sections = [p for p in config.sections() if 'Process' in p]
    for section in sections:
        try:
            lib_name = config.get(section, 'library')
            class_name = config.get(section, 'class')
        except NoOptionError:
            logger.error('Missing library or class option in %s' % section)
            raise
        
        # link to our class
        library = import_module(lib_name)
        class_path = getattr(library, class_name)
        myclass = class_path()
        
        # provide useful object to our class
        myclass.irc = irc
        myclass.config = config
        myclass.logger = logger
        
        # finally start the process
        logger.info('Starting process %s' % section)
        myclass.start()

if __name__ == '__main__':
    main()
