from multiprocessing import Process, Pipe
from time import sleep

class IRCProcess(Process):
    '''Root IRC Class to handle IRC communication and PING/PONG
    
    You can access the IRC communication Pipe from your processes
    simply by accessing self.irc_process.output.recv(), just be
    sure your sleep is inline with IRCProcess.
    '''
    
    def __init__(self):
        self.input, self.output = Pipe()
        super(IRCProcess, self).__init__()
    
    def run(self):
        while True:
            # readsocket performs PING/PONG so we are effectively
            # keeping the connection alive here.
            #
            # We also use Pipe to send the message,
            # your processes can read from this Pipe if they
            # need to listen for IRC messages
            #
            self.input.send(self.irc.readsocket())
            sleep(0.02) # Slow down the loop just a bit to avoid CPU melt ;)
