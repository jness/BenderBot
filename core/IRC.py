import socket
from re import match
from time import sleep
from random import randint
from ConfigParser import ConfigParser
from core.Configuration import get_config

config = get_config()
config_dict = dict(config.items('IRC'))

class IRC:
    def __init__(self, **kwargs):
        # initialize our class with a number of default settings
        kwargs.update(config_dict)
        self.server = kwargs.get('server',"irc.freenode.net")
        self.port = kwargs.get('port',"6667")
        self.channel = kwargs.get('channel',"#BenderTest")
        self.botnick = kwargs.get('botnick',"BenderBot")
        self.nickmsg = kwargs.get('nickmsg', 'Bite my shiny metal ass')
        
    def connect(self):
        print '[INFO] connecting to %s:%s' % (self.server, self.port)
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ircsock.settimeout(5)
        
        # make our connect to the IRC server
        try:
            self.ircsock.connect((self.server, int(self.port)))
        except socket.gaierror as e:
            raise Exception(e)
        except socket.timeout as e:
            raise Exception(e)

        # set our socket back to block to avoid disconnect        
        self.ircsock.settimeout(0)

        # set our nick to self.botnick or attempt to append random numbers
        # to self.botnick
        if not self.__identify():
            self.botnick = '%s%s' % (self.botnick, randint(100, 50000))
            if not self.__identify():
                raise Exception('Unable to set nick')
                    
        self.__joinchannel()
                
    def readsocket(self):
        'Read from a IRC socket and return the results'
        # first lets verify the socket is available still
        self.__checksocket()
        try:
            response = self.ircsock.recv(2048).strip('\n\r')
            self.__checkping(response)
            return response
        except socket.error:
            # empty buffer will return a socket.erroro
            # if the socket is in fact dead the next __checksocket
            # will capture it.
            return None
    
    def quit(self):
        'Quit the IRC session by closing the socket'
        self.ircsock.close()
            
    def sendchannel(self, msg):
        # first lets verify the socket is available still
        self.__checksocket()
        response = self.ircsock.send("PRIVMSG %s :%s\n" % (self.channel, msg))
        return response

    def sendnick(self, nick, msg):
        # first lets verify the socket is available still
        self.__checksocket()
        response = self.ircsock.send("PRIVMSG %s :%s\n" % (nick, msg))
        return response
    
    def __checkping(self, response):
        'Check for PINGs'
        if response:
            if response.find("PING :") != -1:
                print '[INFO] received: %s' % response
                self.__pong(response)
    
    def __checksocket(self):
        'Attempts to access to socket or raises exception'
        try:
            self.ircsock.getsockname()
        except:
            raise Exception('Unable to read from socket')
    
    def __joinchannel(self):
        print '[INFO] joining channel %s' % self.channel
        self.ircsock.send("JOIN %s\n" % self.channel)
    
    def __pong(self, res):
        m = match('PING (.*)', res)
        if match:
            response = self.ircsock.send("PONG %s\r\n" % m.group(1))
            return response
        else:
            raise Exception('Unable to extract message from PING "%"' % res)
    
    def __verify_identify(self):
        readsock = self.ircsock.recv(2048).strip('\n\r')
        if readsock.find("Nickname is already in use") != -1:
            print '[INFO] Nick is already in use'
            return False
        return True
    
    def __identify(self):
        print '[INFO] setting nick to %s' % self.botnick
        self.ircsock.send("USER %s %s %s :%s\n" % (self.botnick, self.botnick,
                                                   self.botnick, self.nickmsg))
        self.ircsock.send("NICK %s\n" % self.botnick)
        sleep(10) # Allow the server sometime to respond
        return self.__verify_identify()