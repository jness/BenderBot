from BenderBot.Configuration import get_config
from BenderBot.Logger import get_logger
from BenderBot.IRC import IRC

from multiprocessing import Process
from time import sleep
import sys

config = get_config()
logger = get_logger(level='INFO')

class IRCProcess(Process):
    '''IRC process responsible for reading from the IRC socket
    and handling PING/PONG'''
    def run(self):
        while True:
            response =  self.irc.readsocket()
            sleep(1)
            
class ExternalProcess(Process):
    '''External Process to handle non IRC processes and respond
    to a channel'''
    def run(self):
        while True:
            # runs your configured module here
            module = __import__(config.get('ExternalProcess', 'module'))
            function = config.get('ExternalProcess', 'function')
            results = eval('module.%s' % function)
            if results:
                self.irc.sendchannel('%s' % results)
                logger.info('sent "%s" to channel' % results)
            sleep(int(config.get('ExternalProcess', 'interval')))

def main():
    '''This is an example script which shows how to use BenderBot,
    and interact with its classes'''
    
    # call our IRC core class to handle everything IRC
    irc = IRC(logger=logger)
    irc.connect()

    # start our Bender Process
    irc_process = IRCProcess()
    irc_process.irc = irc
    irc_process.start()
    
    # start our Example Process
    ex_process = ExternalProcess()
    ex_process.irc = irc
    ex_process.start()

if __name__ == '__main__':
    main()
