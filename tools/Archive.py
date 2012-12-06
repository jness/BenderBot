#!/usr/bin/env python

from BenderBot.BenderMQ import Queue
from BenderBot.Configuration import get_config
from BenderBot.Logger import get_logger

from re import match
from datetime import datetime
import os

# You can alter where logs are placed here
FILELOCATION = './logdir/'

class ArchiveQueue(Queue):
    
    def __init__(self, *args, **kwargs):
        super(ArchiveQueue, self).__init__()
        self.config = get_config()
        self.logger = get_logger(level='INFO')
        self.irccfg = dict(self.config.items('IRC'))
        self.exchange = kwargs.pop('exchange')
        
    def callback(self, ch, method, properties, body):
        for methodname in ['checkPrivmsg', 'checkJoin',
                       'checkPart', 'checkQuit']:
            method = getattr(self, methodname)
            res = method(body)
            if res:
                timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                self.__appendLog((timestamp, res[0], res[1]))
                
    def __appendLog(self, data):
        d = datetime.now()
        filename = '%s-%s-%s.txt' % (d.year, d.month, d.day)
        p = os.path.expanduser(FILELOCATION)
        if not os.path.exists(p):
            os.makedirs(p)

        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.logger.info('Appending message to %s%s' % (p, filename))
        f = open('%s/%s' % (p, filename), 'a+')
        f.write('%s <%s> %s\n' % data)
        f.close()
            
    def checkPrivmsg(self, body):
        m = match(':(.*)!.* PRIVMSG (.*) :(.*)', body)
        if m:
            (nick, channel, message) = m.groups()
            if channel == self.irccfg['channel']:
                msg = (nick, message)
                return msg
    
    def checkJoin(self, body):
        m = match(':(.*)!.* JOIN (.*)', body)
        if m:
            (nick, channel) = m.groups()
            if channel == self.irccfg['channel']:
                msg = (nick, 'has joined %s' % channel)
                return msg
            
    def checkPart(self, body):
        m = match(':(.*)!.* PART (.*)', body)
        if m:
            (nick, channel) = m.groups()
            if channel == self.irccfg['channel']:
                msg = (nick, 'has left %s' % channel)
                return msg
            
    def checkQuit(self, body):
        m = match(':(.*)!.* QUIT', body)
        if m:
            (nick, channel) = m.groups()
            if channel == self.irccfg['channel']:
                msg = (nick, 'has quit')
                return msg
            
def main():
    config = get_config()
    cfg = dict(config.items('RabbitMQ'))
    archive = ArchiveQueue(host=cfg['host'],
                           exchange='irc')
    archive.subscribe()
    
if __name__ == '__main__':
    main()