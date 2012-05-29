from BenderBot.Configuration import get_config
from BenderBot.Logger import get_logger
from BenderBot.IRC import IRC

from ConfigParser import NoOptionError, NoSectionError
from multiprocessing import Process
from time import sleep

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
        # runs your configured module here
        try:
            mylib = config.get('ExternalProcess', 'library')
            myfunction = config.get('ExternalProcess', 'function')
            myintreval = config.get('ExternalProcess', 'interval')
            
        except NoOptionError as e:
            logger.warning('Missing library, function, or intreval options')
            logger.warning('Killing ExternalProcess')
            return 1
        
        except NoSectionError as e:
            logger.warning('Missing ExternalProcess section')
            logger.warning('Killing ExternalProcess')
            return 1
            
        logger.debug('importig python module "%s"' % mylib)
        lib = __import__(mylib)
        
        while True:
            logger.debug('running function "%s from %s"' % (myfunction, mylib))
            results = eval('lib.%s' % myfunction)
            
            if results:
                logger.info('sent "%s" to channel' % results)
                self.irc.sendchannel('%s' % results)
            sleep(int(myintreval))

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
