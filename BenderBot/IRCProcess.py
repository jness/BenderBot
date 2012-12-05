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

class IRCProcess(Process):
    '''Root IRC Class to handle IRC communication and PING/PONG'''
    
    def __init__(self, *args, **kwargs):
        self.logger = kwargs.pop('logger')
        self.config = kwargs.pop('config')
        self.queue = kwargs.pop('queue')
        self.irc = kwargs.pop('irc')
        
        # set the write sub child method for this process
        target = kwargs.pop('target')
        if target == 'read':
            kwargs['target'] = self.irc_read
        elif target == 'write':
            kwargs['target'] = self.irc_write
        
        super(IRCProcess, self).__init__(*args, **kwargs)
        
    def irc_read(self):
        '''readsocket performs PING/PONG so we are effectively
            keeping the connection alive here.'''
        while True:
            msg = self.irc.readsocket()
            if msg:
                self.logger.debug("Adding Message to RabbitMQ: %s" % msg)
                self.queue.publish(msg)
            sleep(0.02) # Slow down the loop just a bit to avoid CPU melt ;)

    def irc_write(self):
        '''write messages to the channel for anything in RabbitMQ'''
        cfg = dict(self.config.items('RabbitMQ'))
        queue = MyQueue(host=cfg['host'], exchange='ircwrite',
                        irc=self.irc)
        queue.subscribe()