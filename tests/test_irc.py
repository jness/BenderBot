from BenderBot.IRC import IRC
from BenderBot.Configuration import get_config
import unittest

class LoggerTest(unittest.TestCase):

    def setUp(self):
        self.config = get_config()
        
    def test_sendchannel(self):
        irc = IRC(**dict(self.config.items('IRC')))
        irc.connect()
        self.assertTrue(irc.sendchannel('unittest'))
        irc.quit()
        
    def test_sendnick(self):
        irc = IRC(**dict(self.config.items('IRC')))
        irc.connect()
        nick = self.config.get('IRC', 'botnick')
        self.assertTrue(irc.sendnick(nick, 'unittest'))
        irc.quit()
        
    def test_existing_nick(self):
        options = dict(self.config.items('IRC'))
        options['botnick'] = 'nessy'
        irc = IRC(**options)
        irc.connect()
        irc.quit()
        
    def test_identify(self):
        options = dict(self.config.items('IRC'))
        options['botnick'] = 'nessy'
        irc = IRC(**options)
        irc.connect()
        irc.identify('pass')
        irc.quit()

if __name__ == '__main__':
    unittest.main()