from BenderBot.Configuration import get_config
from BenderBot.Logger import get_logger
from BenderBot.IRCProcess import IRCProcess
from BenderBot.BenderMQ import Queue
from BenderBot.IRC import IRC
from time import sleep
import argparse
import sys
import signal

def quit(signal, frame):
    'Capture SIGINT ctrl+c'
    sys.exit(0)

def main():
    '''This is the main BenderBot script, it ties all the pieces
    together and runs our active bot'''
    
    # handle CTRL+C nicely
    signal.signal(signal.SIGINT, quit)
    
    # get our configuration
    config = get_config()

    # process args for debug
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action="store_true", dest="debug",
                        default=False, help='Turn on verbose debugging')
    args = parser.parse_args()
    
    # set logging level based on argparse
    if args.debug:
        logger = get_logger(level='DEBUG')
    else:
        logger = get_logger(level='INFO')

    # Connect to the RabbitMQ server
    cfg = dict(config.items('RabbitMQ'))
    queue = Queue(**cfg)
    
    # Connec to IRC
    cfg = dict(config.items('IRC'))
    irc = IRC(logger=logger, queue=queue, **cfg)
    irc.connect()
    irc.joinchannel()

    # Start the IRC read process that handles PING/PONG,
    # and adding any IRC messages to RabbitMQ
    logger.info('Starting IRCProcess Read')
    
    irc_read = IRCProcess(name='irc_read', target='read',
                          logger=logger, config=config, queue=queue, irc=irc)
    irc_read.daemon = True
    irc_read.start()
    
    # Start the IRC write process
    logger.info('Starting IRCProcess Write')
    irc_write = IRCProcess(name='irc_write', target='write',
                           logger=logger, config=config, queue=queue, irc=irc)
    irc_write.daemon = True
    irc_write.start()
    
    # keep running as long as subprocesses are good
    while irc_write.is_alive() and irc_read.is_alive():
        sleep(1)

if __name__ == '__main__':
    main()
