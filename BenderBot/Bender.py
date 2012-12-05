from BenderBot.Configuration import get_config
from BenderBot.Logger import get_logger
from BenderBot.IRC import IRC
from BenderBot.IRCProcess import IRCRead, IRCWrite
from BenderBot.BenderMQ import Queue

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
    logger.info('Starting IRCRead')
    irc_read = IRCRead(irc=irc, logger=logger,
                          config=config, queue=queue)
    irc_read.start()
    
    # Start the IRC write process
    logger.info('Starting IRCWrite')
    irc_write = IRCWrite(irc=irc, logger=logger,
                          config=config)
    irc_write.start()
    
    # Keep an eye on our two Processes
    # so we can kill the script if need be.
    while True:
        if not irc_read.is_alive():
            logger.error('IRCRead Process died..')
            irc_write.terminate()
            raise Exception('IRCRead Process died')
        if not irc_write.is_alive():
            logger.error('IRCWrite Process died..')
            irc_read.terminate()
            raise Exception('IRCWrite Process died')

if __name__ == '__main__':
    main()
