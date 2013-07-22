import pika
from pika.exceptions import *
import sys

class Queue(object):
    
    def __init__(self, **kwargs):
        self.host = kwargs.get('host', 'localhost')
        self.port = int(kwargs.get('port', 5672))
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.exchange = kwargs.get('exchange')
          
    def __connect(self):
        '''Connect to a RabbitMQ server'''
		kwargs = dict(host=self.host, port=self.port)
        try:
			if self.username and self.password:
				credentials = pika.PlainCredentials(self.username, self.password)
				kwargs['credentials'] = credentials
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                **kwargs))
        except AMQPConnectionError, e:
            raise Exception('Unable to connect to %s: %s' % (self.host, e))
        
    def __disconnect(self):
        '''Disconnect from a RabbitMQ server'''
        self.connection.close()
        
    def __channel(self):
        '''Setup the channel'''
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange,
                         type='fanout')
        
    def publish(self, message):
        '''Publish a message to the exchange'''
        self.__connect()
        self.__channel()
        self.channel.basic_publish(exchange=self.exchange,
                              routing_key='',
                              body=message)
        self.__disconnect()
        
    def callback(self, ch, method, properties, body):
        '''Override me to do something useful'''
        print " [x] %r" % (body,)
    
    def subscribe(self):
        '''Subscribe to a message exchange'''
        self.__connect()
        self.__channel()
        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(exchange=self.exchange,
                   queue=queue_name)
        
        self.channel.basic_consume(self.callback,
                      queue=queue_name,
                      no_ack=True)
    
        self.channel.start_consuming()
