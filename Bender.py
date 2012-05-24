#!/usr/bin/env python
from multiprocessing import Process
from time import sleep
from core.IRC import IRC
from core.Configuration import get_config

# imports for example Github process
from urllib2 import urlopen
from json import loads

config = get_config()

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
            print '[INFO] running Custom Github Process'
            res = urlopen(config.get('Github', 'url')).read()
            repo = loads(res)
            self.irc.sendchannel('%s last pushed @ %s' % (
                                            repo['name'], repo['pushed_at']))
            sleep(300)

def main():
    '''Our main function which is called on script start'''
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
