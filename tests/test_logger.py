from BenderBot.Logger import get_logger
import unittest

class LoggerTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_logger_info(self):
        logger = get_logger(level='INFO')
        self.assertTrue(logger)
        
    def test_logger_debug(self):
        logger = get_logger(level='DEBUG')
        self.assertTrue(logger)

if __name__ == '__main__':
    unittest.main()