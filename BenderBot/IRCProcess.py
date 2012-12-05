from multiprocessing import Process
from time import sleep
from BenderBot.BenderMQ import Queue

class MyQueue(Queue):
    '''My Custom Queue for sending messages on subscribe'''
    def __init__(self, **kwargs):
        super(MyQueue, self).__init__()
        self.irc = kwargs.pop('irc')
        self.exchange = kwargs.pop('exchange')
        
    def callback(self, ch, method, properties, body):
        self.irc.sendchannel(body)

class IRCRead(Process):
    '''Root IRC Class to handle IRC communication and PING/PONG'''
    
    def __init__(self, **kwargs):
        self.logger = kwargs.pop('logger')
        self.config = kwargs.pop('config')
        self.queue = kwargs.pop('queue')
        self.irc = kwargs.pop('irc')
        
        super(IRCRead, self).__init__()
           
    def run(self):
        while True:
            # readsocket performs PING/PONG so we are effectively
            # keeping the connection alive here.
            #
            # We also use Queue to append messages.
            # Your process can read from this Queue if they
            # need to listen for IRC messages, to do
            # use self.queue.get() and be sure your Process
            # configuration has 'listen' set to True.
            #
            msg = self.irc.readsocket()
            if msg:
                self.logger.debug("Adding Message to RabbitMQ: %s" % msg)
                self.queue.publish(msg)
            sleep(0.02) # Slow down the loop just a bit to avoid CPU melt ;)

class IRCWrite(Process):
    '''Root IRC Class to handle incoming messages from RabbitMQ'''
    
    def __init__(self, **kwargs):
        self.logger = kwargs.pop('logger')
        self.irc = kwargs.pop('irc')
        self.config = kwargs.pop('config')
        
        super(IRCWrite, self).__init__()
           
    def run(self):
        cfg = dict(self.config.items('RabbitMQ'))
        queue = MyQueue(host=cfg['host'], exchange='ircwrite',
                        irc=self.irc)
        queue.subscribe()
        