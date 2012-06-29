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
            msg = self.irc_process.output.recv()
            
            # it is very important to keep your sleep time in line
            # with the IRC Process sleep time, by default this is 0.02
            # seconds
            sleep(0.02) # Slow down the loop just a bit to avoid CPU melt ;)
