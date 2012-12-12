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
    'Quit function'
    sys.exit(0)

def main():
    '''This is the main BenderBot script, it ties all the pieces
    together and runs our active bot'''
    
    # handle CTRL+C nicely
    signal.signal(signal.SIGINT, quit)
    
    # handle Linux kill SIGTERM
    signal.signal(signal.SIGTERM, quit)

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
    
    # Connect to IRC
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
    
    # keep an eye on our IRC Read and Write processes
    while irc_write.is_alive() and irc_read.is_alive():
        # take a nap ;)
        sleep(1)

    # the only way we end up here is if irc_write or irc_read died,
    # lets report the status of each and shutdown
    write, read = (irc_write.is_alive(), irc_read.is_alive())
    logger.warn('IRC Write process alive: %s' % write)
    logger.warn('IRC Read process alive: %s' % read)
    logger.info('BenderBot is shutting down')

if __name__ == '__main__':
    main()
