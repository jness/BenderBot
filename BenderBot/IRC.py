import socket
from re import match
from time import sleep
from random import randint
from ConfigParser import ConfigParser
from BenderBot.Configuration import get_config

# read in our configuration for passing to kwargs
config = get_config()
config_dict = dict(config.items('IRC'))

class IRC:
    def __init__(self, **kwargs):
        '''called when the class is first sourced.
        __init__ will handle setting up IRC settings pulled in form
        the configuration or default with the use of kwargs.get()'''
        kwargs.update(config_dict)
        self.server = kwargs.get('server',"irc.freenode.net")
        self.port = kwargs.get('port',"6667")
        self.channel = kwargs.get('channel',"#BenderTest")
        self.botnick = kwargs.get('botnick',"BenderBot")
        self.nickmsg = kwargs.get('nickmsg', 'Bite my shiny metal ass')
        
    def connect(self):
        '''should be called after your source the IRC class,
        this method will connect to the IRC server, set the nick, and
        join a channel all based on the configuration'''
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
        '''will read from the IRC socket,
        it will return the socket data or if the socket buffer
        is empty it will return None'''
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
        'will close the current socket'
        self.ircsock.close()
            
    def sendchannel(self, msg):
        '''send a message to the joined channel,
        this is the channel configured in config/bot.conf'''
        # first lets verify the socket is available still
        self.__checksocket()
        response = self.ircsock.send("PRIVMSG %s :%s\n" % (self.channel, msg))
        return response

    def sendnick(self, nick, msg):
        '''will send a private message to the IRC user''' 
        # first lets verify the socket is available still
        self.__checksocket()
        response = self.ircsock.send("PRIVMSG %s :%s\n" % (nick, msg))
        return response
    
    def __checkping(self, response):
        'Private method that will check a response for PING'
        if response:
            if response.find("PING :") != -1:
                print '[INFO] received: %s' % response
                self.__pong(response)
    
    def __checksocket(self):
        'Private method that attempts to access the socket or raises exception'
        try:
            self.ircsock.getsockname()
        except:
            raise Exception('Unable to read from socket')
    
    def __joinchannel(self):
        'Private method used to join a IRC channel'
        print '[INFO] joining channel %s' % self.channel
        self.ircsock.send("JOIN %s\n" % self.channel)
    
    def __pong(self, response):
        'Private method that will send PONG to requesting service'
        m = match('PING (.*)', response)
        if match:
            pong = self.ircsock.send("PONG %s\r\n" % m.group(1))
            return pong
        else:
            raise Exception('Unable to extract message from PING "%"' % res)
    
    def __verify_identify(self):
        'Private method that checkes a response for Nick already in use'
        response = self.readsocket()
        if response.find("Nickname is already in use") != -1:
            print '[INFO] Nick is already in use'
            return False
        return True
    
    def __identify(self):
        '''Private method which sets USER and NICK, will then call
        __verify_identify to be sure not already in use'''
        print '[INFO] setting nick to %s' % self.botnick
        self.ircsock.send("USER %s %s %s :%s\n" % (self.botnick, self.botnick,
                                                   self.botnick, self.nickmsg))
        self.ircsock.send("NICK %s\n" % self.botnick)
        sleep(10) # Allow the server sometime to respond
        return self.__verify_identify()
