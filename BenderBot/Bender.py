from BenderBot.Configuration import get_config
from BenderBot.Logger import get_logger
from BenderBot.IRC import IRC
from BenderBot.IRCProcess import IRCProcess

from ConfigParser import NoOptionError, NoSectionError
from multiprocessing import Process, Queue
from importlib import import_module
from time import sleep
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
        
    # create a Queue to hold all IRC messages
    queue = Queue()
        
    # call our IRC core class to handle everything IRC
    irc = IRC(logger=logger, queue=queue)
    irc.connect()
    #irc.queue = queue
    
    # find all of our processes
    important_processes = []
    processes = []
    sections = [p for p in config.sections() if 'Process' in p]
    
    # start the IRC root process that handles PING/PONG
    irc_process = IRCProcess(queue=queue)
    irc_process.irc = irc
    
    # start the root process
    logger.info('Starting root IRC process')
    irc_process.start()
    
    # add root process to listing
    processes.append(irc_process)
    important_processes.append(irc_process)
    
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
        myclass.irc_process = irc_process
        
        # finally start the process
        logger.info('Starting process %s' % section)
        myclass.start()
       
        # see if this process is important and needs to be watched
        processes.append(myclass)
        try:
            important = config.get(section, 'important')
        except NoOptionError:
            important = False   
        if important:
            important_processes.append(myclass)
            
    # a loop to watch our import processes
    while True:
        for p in important_processes:
            if not p.is_alive():
                for process in processes:
                    process.terminate()
                raise Exception('One of your important processes died')
            sleep(5)
        
if __name__ == '__main__':
    main()
