from BenderBot.BenderProcess import BenderProcess
from BenderBot.Configuration import get_config
import BaseHTTPServer
from time import sleep
from json import loads

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    'Custom HTTP Handler for BenderBot POSTs'
    
    def __checkJSON(self):
        'verify the JSON can be loaded'
        try:
            self.data = loads(self.data_string)
            self.logger.debug('successfully loaded json from http post')
        except:
            self.logger.debug('unable to load json from http post')
            self.send_response(500)
            return False
        else:
            return True
        
    def __checkContent(self):
        'Verify all needed keys are in the dict'
        if self.data.get('key') and self.data.get('message'):
            self.logger.debug('verified json object has key and message keys')
            return True
        else:
            self.logger.debug('missing key or message objects in json keys')
            self.send_response(500)
            return False
        
    def do_POST(self):
        # BaseHTTPRequestHandler uses old style classes and I can not
        # super the __init__, setting a few globals to address
        global message
        global logger
        self.logger = logger
        global config
        self.config = config
        
        self.logger.debug('received http post using BenderBot_HTTPListener')
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        if self.__checkJSON():
            if self.__checkContent():
                key = self.config.get('HTTPListener', 'key')
                if str(self.data['key']) == str(key):
                    self.send_response(200)
                    message = self.data['message']
                else:
                    self.logger.debug('invalid key in json data')
                    self.send_response(403)
                    
    def log_message(self, format, *args):
        return

class Listener(BenderProcess):
    
    def run(self):
        # BaseHTTPRequestHandler uses old style classes and I can not
        # super the __init__, setting a few globals to address
        global message
        global logger
        logger = self.logger
        global config
        config = self.config
        
        port = self.config.get('HTTPListener', 'port')
        host = self.config.get('HTTPListener', 'host')
        httpd = BaseHTTPServer.HTTPServer((host, int(port)), MyHandler)
        while True:
            message = None
            httpd.handle_request()
            if message:
                self.irc.sendchannel(message)
            sleep(0.02) # Slow down the loop just a bit to avoid CPU melt ;)