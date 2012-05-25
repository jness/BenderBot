#!/usr/bin/env python
#
# This is an example script to demonstrate
# how to use the BenderBot IRC class to construct
# and custom IRC Bot.

from multiprocessing import Process
from time import sleep
from BenderBot.IRC import IRC
from BenderBot.Configuration import get_config
from BenderBot.Logger import get_logger

# imports for example Github process
from urllib2 import urlopen
from json import loads

config = get_config()
logger = get_logger(level='INFO')

class Bender(Process):
    'Bender is a class that reads from the IRC socket'
    def run(self):
        '''Here is where we perform the loop that reads
        data from the IRC server, we can handle IRC task here'''
        while True:
            response =  self.irc.readsocket()
            sleep(1)
            
class Github(Process):
    'A example Process for checking a Github repo using API'
    def run(self):
        while True:
            logger.info('running custom github process')
            res = urlopen('https://api.github.com/repos/jness/BenderBot').read()
            repo = loads(res)
            msg = '%s last pushed @ %s' % (repo['name'], repo['pushed_at'])
            self.irc.sendchannel(msg)
            logger.info('sent "%s" to channel' % msg)
            sleep(300)

def main():
    '''This is an example script which shows how to use BenderBot,
    and interact with its classes'''
    
    # call our IRC core class to handle everything IRC
    irc = IRC()
    irc.connect()

    # start our Bender Process
    bender = Bender()
    bender.irc = irc
    bender.start()
    
    # start our Weather Example Process
    github = Github()
    github.irc = irc
    github.start()

if __name__ == '__main__':
    main()
