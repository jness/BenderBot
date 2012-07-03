from multiprocessing import Process, Queue
from time import sleep

class IRCProcess(Process):
    '''Root IRC Class to handle IRC communication and PING/PONG
    
    You can access the IRC communication Pipe from your processes
    simply by accessing self.irc_process.output.recv(), just be
    sure your sleep is inline with IRCProcess.
    '''
    
    def __init__(self):
        self.queue = Queue()
        super(IRCProcess, self).__init__()
    
    def run(self):
        while True:
            # readsocket performs PING/PONG so we are effectively
            # keeping the connection alive here.
            #
            # We also use Queue to append messages.
            # Your process can read from this Queue if they
            # need to listen for IRC messages, to do
            # use self.irc_process.queue.get()
            #
            msg = self.irc.readsocket()
            if msg:
                self.queue.put(msg)
            sleep(0.02) # Slow down the loop just a bit to avoid CPU melt ;)
