import socket
from re import match
from time import sleep
from random import randint
from ConfigParser import ConfigParser
from BenderBot.Configuration import get_config
from BenderBot.Logger import get_logger

config = get_config()
config_dict = dict(config.items('IRC'))

class IRC:
    def __init__(self, **kwargs):
        '''Our initializer that sets our server attributes'''
        kwargs.update(config_dict)
        self.server = kwargs.get('server',"irc.freenode.net")
        self.port = kwargs.get('port',"6667")
        self.channel = kwargs.get('channel',"#BenderTest")
        self.botnick = kwargs.get('botnick',"BenderBot")
        self.nickmsg = kwargs.get('nickmsg', 'Bite my shiny metal ass')
        self.logger = kwargs.get('logger', get_logger())
        
    def connect(self):
        ''' The ``connect`` method performs a couple of key actions.
        Using the attributes set in ``__init__`` we are able to connect
        to the IRC server, set the users nick, and join a channel.
        
        - **method usage**::

            >>> from BenderBot.IRC import IRC
            >>> irc = IRC()
            >>> irc.connect()
            [INFO] connecting to irc.freenode.net:6667
            [INFO] setting nick to BenderBot
            [INFO] joining channel #bender-test
        
        '''
        self.logger.info('connecting to %s:%s' % (self.server, self.port))
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
        '''The ``readsocket`` method will first validate a socket is
        available by running ``__checksocket``, we will then create a
        buffer and read one byte from the socket until we reach a CRLF.
        This is in accordance to RFC1459:
        http://tools.ietf.org/html/rfc1459#section-2.3
        
        Since we read from the buffer here we also need to check for
        **PING**, we do this with ``__checkping``.
        
        The method will then return you the buffer,
        or None if the buffer was empty:
        
        - **method usage**::
        
            >>> irc.readsocket()
            ':user1!~user1@127.0.0.1 PRIVMSG #bender-test :Hello BenderBot '
        
        '''
        self.__checksocket()
        buffer = ''
        while True:
            try:
                response = self.ircsock.recv(1)
            except socket.error:
                # empty buffer will return a socket.error
                # if the socket is in fact dead the next __checksocket
                # will capture it.
                return None
                
            buffer += response
            if buffer.find('\r\n') != -1:
                res = buffer.strip('\r\n')
                self.__checkping(res)
                return res
    
    def quit(self):
        '''the ``quit`` method will close the current socket
        
        - **method usage**::
            
            >>> irc.quit()
        '''
        self.ircsock.close()
            
    def sendchannel(self, msg):
        '''the ``sendchannel`` method sends a message to the current
        joined channel defined by ``self.channel``. Before we send a message
        we first confirm the socket is available with ``__checksocket()``
        
        - **method usage**
        
            >>> irc.sendchannel('Bite my shiny metal ass meatbag!')
            55
        '''
        self.__checksocket()
        self.logger.info('sending: PRIVMSG %s :%s' % (self.channel, msg))
        response = self.ircsock.send("PRIVMSG %s :%s\n" % (self.channel, msg))
        return response

    def sendnick(self, nick, msg):
        '''the ``sendnick`` method sends a message to a specific user nick.
        Before we send a message we first confirm the socket is available
        with ``__checksocket()``
        
        - **method usage**
        
            >>> irc.sendnick('user1', 'Bite my shiny metal ass meatbag!')
            48
        '''
        self.__checksocket()
        self.logger.info('sending: PRIVMSG %s :%s' % (nick, msg))
        response = self.ircsock.send("PRIVMSG %s :%s\n" % (nick, msg))
        return response
    
    def __checkping(self, response):
        'Private method that will check a response for PING'
        if response:
            if response.find("PING :") != -1:
                self.logger.debug('received: %s' % response)
                self.__pong(response)
    
    def __checksocket(self):
        'Private method that attempts to access the socket or raises exception'
        try:
            self.ircsock.getsockname()
        except:
            raise Exception('Unable to read from socket')
    
    def __joinchannel(self):
        'Private method used to join a IRC channel'
        self.logger.info('joining channel %s' % self.channel)
        self.ircsock.send("JOIN %s\n" % self.channel)
    
    def __pong(self, response):
        'Private method that will send PONG to requesting service'
        m = match('PING (.*)', response)
        if match:
            self.logger.debug('sending: PONG %s' % m.group(1))
            pong = self.ircsock.send("PONG %s\r\n" % m.group(1))
            return pong
        else:
            raise Exception('Unable to extract message from PING "%"' % res)
    
    def __verify_identify(self):
        'Private method that checkes a response for Nick already in use'
        response = self.readsocket()
        if response.find("Nickname is already in use") != -1:
            self.logger.warning('Nick is already in use')
            return False
        return True
    
    def __identify(self):
        '''Private method which sets USER and NICK, will then call
        __verify_identify to be sure not already in use'''
        self.logger.info('setting nick to %s' % self.botnick)
        self.ircsock.send("USER %s %s %s :%s\n" % (self.botnick, self.botnick,
                                                   self.botnick, self.nickmsg))
        self.ircsock.send("NICK %s\n" % self.botnick)
        sleep(10) # Allow the server sometime to respond
        return self.__verify_identify()
