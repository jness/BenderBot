from BenderBot.Configuration import get_config
from BenderBot.Logger import get_logger
from BenderBot.IRC import IRC

from ConfigParser import NoOptionError, NoSectionError
from multiprocessing import Process
from time import sleep
from importlib import import_module
import argparse

class IRCProcess(Process):
    '''IRC process responsible for reading from the IRC socket
    and handling PING/PONG'''
    def run(self):
        
        try:
            mylib = config.get('IRCProcess', 'library')
            myfunction = config.get('IRCProcess', 'function')
            
        except NoOptionError as e:
            logger.warning('IRCProcess missing library or function options')
            mylib = None
            myfunction = None
        
        except NoSectionError as e:
            logger.warning('missing IRCProcess section')
            mylib = None
            myfunction = None
        
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
            logger.warning(
               'ExternalProcess missing library, function, or intreval options')
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
            func = getattr(lib, myfunction)
            results = func()
            
            if results:
                self.irc.sendchannel('%s' % results)
            sleep(int(myintreval))

def main():
    '''This is an example script which shows how to use BenderBot,
    and interact with its classes'''

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
