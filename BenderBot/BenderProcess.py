from multiprocessing import Process
from time import sleep

class BenderProcess(Process):
    '''A base Process for easy subclassing'''
    
    def __init__(self):
        super(BenderProcess, self).__init__()
    
    def run(self):
        while True:
            # Example on how to read from the IRC Process socket
            # and get IRC communication from server
            msg = self.irc_process.queue.get()
            
            sleep(0.02) # Slow down the loop just a bit to avoid CPU melt ;)
