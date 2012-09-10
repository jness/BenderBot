from BenderBot.IRC import IRC
from multiprocessing import Queue
from BenderBot.Configuration import get_config
import unittest

class LoggerTest(unittest.TestCase):

    def setUp(self):
        self.config = get_config(cfg_name='config/bender.conf-example')
        self.irc = IRC(**dict(self.config.items('IRC')))
        self.irc.connect()
        
    def test_sendchannel(self):
        self.assertTrue(self.irc.sendchannel('unittest'))
        self.irc.quit()
        
    def test_sendnick(self):
        nick = self.config.get('IRC', 'botnick')
        self.assertTrue(self.irc.sendnick(nick, 'unittest'))
        self.irc.quit()

if __name__ == '__main__':
    unittest.main()