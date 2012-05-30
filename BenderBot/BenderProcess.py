from multiprocessing import Process
from time import sleep

class BenderProcess(Process):
    '''A base Process for easy subclassing'''
    
    def __init__(self):
        super(BenderProcess, self).__init__()
    
    def run(self):
        while True:
            # readsocket performs PING/PONG so we are effectively
            # keeping the connection alive here.
            response =  self.irc.readsocket()
            if response:
                self.logger.debug(response)
            sleep(0.02) # Slow down the loop just a bit to avoid CPU melt ;)
