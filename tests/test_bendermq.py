from BenderBot.BenderMQ import Queue
from BenderBot.Configuration import get_config
import unittest

class BenderMQTest(unittest.TestCase):

    def setUp(self):
        self.config = get_config()
        
    def test_publish(self):
        queue = Queue(**dict(self.config.items('RabbitMQ')))
        queue.publish('test message')

if __name__ == '__main__':
    unittest.main()