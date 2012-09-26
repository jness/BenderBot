from BenderBot.Configuration import get_config
from BenderBot.Logger import get_logger
from BenderBot.IRC import IRC
from BenderBot.IRCProcess import IRCProcess
from BenderBot.Dispatcher import Dispatcher

from ConfigParser import NoOptionError, NoSectionError
from multiprocessing import Queue
from time import sleep
import argparse
import sys, os
import signal

def quit(signal, frame):
    'Capture SIGINT ctrl+c'
    sys.exit(0)

def main():
    '''This is the main BenderBot script, it ties all the pieces
    together and runs our active bot'''
    
    # handle CTRL+C nicely
    signal.signal(signal.SIGINT, quit)

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

    # show PIDs if in debug mode        
    logger.info('Bender pid is %s' % os.getpid())
        
    # create a Queue to hold all IRC messages
    queue = Queue()
        
    # Start the IRC root process that handles PING/PONG,
    logger.info('Starting IRCProcess')
    irc_process = IRCProcess(queue=queue, logger=logger, config=config)
    irc_process._pid = os.getpid()
    irc_process.start()
    
    # Start our Dispatcher
    logger.info('Starting Dispatcher')
    dispatcher = Dispatcher(logger=logger, config=config)
    dispatcher.irc = irc_process.get_irc()
    dispatcher.queue = queue
    dispatcher._pid = os.getpid()
    dispatcher.start()
    
    # loop to watch our irc_process
    while True:
        if not irc_process.is_alive():
            logger.info('IRCProcess died...')
            os.killpg(os.getpid(), signal.SIGKILL)
        if not dispatcher.is_alive() or dispatcher.exit.is_set():
            logger.info('Dispatcher died...')
            os.killpg(os.getpid(), signal.SIGKILL)
        sleep(5)
        
if __name__ == '__main__':
    main()
