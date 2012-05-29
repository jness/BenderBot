from BenderBot.Configuration import get_config
from BenderBot.Logger import get_logger
from BenderBot.IRC import IRC

from ConfigParser import NoOptionError, NoSectionError
from multiprocessing import Process
from time import sleep
from importlib import import_module

class IRCProcess(Process):
    '''IRC process responsible for reading from the IRC socket
    and handling PING/PONG'''
    def run(self):
        
        try:
            mylib = config.get('IRCProcess', 'library')
            myfunction = config.get('IRCProcess', 'function')
            
        except NoOptionError as e:
            logger.warning('missing library or function options')
        
        except NoSectionError as e:
            logger.warning('missing IRCProcess section')
        
        if mylib:
            logger.debug('importig python module "%s"' % mylib)
            lib = import_module(mylib)
        
        while True:
            response =  self.irc.readsocket()
            
            # if we have a custom IRCProcess it will run here
            if mylib and myfunction and response:
                func = getattr(lib, myfunction)
                msg = func(response)
                if msg:
                    self.irc.sendchannel(msg)
                
            sleep(0.05) # Slow down the loop just a bit to avoid CPU melt ;)
        
class ExternalProcess(Process):
    '''External Process to handle non IRC processes and respond
    to a channel'''
    def run(self):
        
        try:
            mylib = config.get('ExternalProcess', 'library')
            myfunction = config.get('ExternalProcess', 'function')
            myintreval = config.get('ExternalProcess', 'interval')
            
        except NoOptionError as e:
            logger.warning('missing library, function, or intreval options')
            logger.warning('killing ExternalProcess')
            return 1
        
        except NoSectionError as e:
            logger.warning('missing ExternalProcess section')
            logger.warning('killing ExternalProcess')
            return 1
            
        logger.debug('importig python module "%s"' % mylib)
        lib = import_module(mylib)
        
        while True:
            logger.debug('running function "%s from %s"' % (myfunction, mylib))
            results = eval('lib.%s' % myfunction)
            
            if results:
                self.irc.sendchannel('%s' % results)
            sleep(int(myintreval))

def main():
    '''This is an example script which shows how to use BenderBot,
    and interact with its classes'''

    global config, logger    
    config = get_config()
    logger = get_logger(level='INFO')
    
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
