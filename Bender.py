#!/usr/bin/env python
from multiprocessing import Process
import ConfigParser
from time import sleep

from Lib.irctoolbox import IRC

class IRCbot(Process):
    def run(self):
        while True:
            # verify socket before reading
            self.ircsock = check_socket(self.ircsock, self.irc)
            
            # go ahead and recv
            data = self.ircsock.recv(2048).strip('\n\r')
            if data.find("PING :") != -1:
                print '[INFO] received: %s' % str(data)
                self.irc.ping()

def connect(irc):
    '''Simply connect to the IRC server'''
    ircsock = irc.connect()
    return ircsock

def check_socket(ircsock, irc):
    '''Only way to verify a socket is to read from it'''
    try:
        ircsock.getsockname()
    except:
        ircsock, irc = connect()
    return ircsock

def main():
    '''Our main function which is call on script start'''

    # Load our Configuration
    config = ConfigParser.ConfigParser()
    config.readfp(open('Config/bot.conf'))

    # link to our IRC Class
    irc = IRC()
    irc.server = config.get('IRC', 'server')
    irc.port = config.get('IRC', 'port')
    irc.channel = config.get('IRC', 'channel')
    irc.botnick = config.get('IRC', 'botnick')
    irc.altbotnick = config.get('IRC', 'altbotnick')
    ircsock = connect(irc)

    # Start IRC Loop
    I = IRCbot()
    I.ircsock = ircsock
    I.irc = irc
    I.start()

    #
    # Start our own process below
    # these process can check external API and post
    # to the channel or pretty much anything you like.
    #
    # For example I will use Google's Weather XML 
    # to inform the channel of the Weather in Austin TX.
    #
    while True:
        from urllib2 import urlopen
        from xml.dom import minidom
        
        check_interval = config.get('IRC', 'check_interval')
        weather_url = config.get('WEATHER', 'url')

        print '[INFO] custom process running'
        dom = minidom.parse(urlopen(weather_url))

        current = dom.getElementsByTagName('current_conditions')
        temp = current[0].getElementsByTagName('temp_f')[0].getAttribute('data')

        irc.post('Current temperature in Austin Texas is %sF' % temp)

        # sleep until next iteration
        sleep(int(check_interval))


if __name__ == '__main__':
    main()
