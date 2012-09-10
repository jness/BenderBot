from BenderBot.Configuration import get_config
import unittest

class ConfigTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_config_found(self):
        self.config = get_config(cfg_name='config/bender.conf-example')
        port = self.config.get('IRC', 'port')
        self.assertEqual(port, '6667')
        
    def test_config_notfound(self):
        self.assertRaises(Exception, get_config, cfg_name='NO_FILE_HERE')
        
if __name__ == '__main__':
    unittest.main()