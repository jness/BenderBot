from multiprocessing import Process, Queue, Event
from ConfigParser import NoOptionError, NoSectionError
from importlib import import_module
from time import sleep
import os

class Dispatcher(Process):
    ''' The Dispatcher for starting up all configured processes in
    ~/.bender.conf, '''

    def __init__(self, **kwargs):
        self.logger = kwargs.pop('logger')
        self.config = kwargs.pop('config')
        super(Dispatcher, self).__init__()
        self.exit = Event()
        
    def __setup(self):
        'Setup before process start'
        self.listen_processes = []
        self.important_processes = []
        self.processes = []
        self.sections = [p for p in self.config.sections() if 'Process' in p]
        
    def __start(self):
        'Start each of our configured processes'
        for section in self.sections:
            try:
                lib_name = self.config.get(section, 'library')
                class_name = self.config.get(section, 'class')
            except NoOptionError:
                self.logger.error('Missing library or class option in %s' % \
                                   section)
                raise
            
            # link to our class
            library = import_module(lib_name)
            class_path = getattr(library, class_name)
            myclass = class_path()
            
            # provide useful object to our class
            myclass.irc = self.irc
            myclass.config = self.config
            myclass.logger = self.logger
            myclass.queue = Queue()
            
            # if class needs access to the IRC message queue
            # create it here
            try:
                listen = self.config.get(section, 'listen')
                if listen:
                    self.listen_processes.append(myclass)
            except NoOptionError:
                pass
            
            # finally start the process
            self.logger.info('Starting process %s' % section)
            myclass.start()
            self.logger.info('Process %s pid is %s' % (section, myclass.pid))
            
            # see if this process is important and needs to be watched
            self.processes.append(myclass)
            try:
                important = self.config.getboolean(section, 'important')
            except NoOptionError:
                important = False
            if important:
                self.important_processes.append(myclass)
                
    def __queueupdate(self, msg):
        'Update processes that require IRC message queue access'
        for process in self.listen_processes:
            if msg:
                process.queue.put(msg)
                
    def __monitor(self):
        'Monitor our important processes'
        for process in self.processes:
            if not process.is_alive():
                self.logger.warn('Process %s is not alive' % process)
                item = self.processes.index(process)
                del(self.processes[item])
                if process in self.important_processes:
                    self.logger.error('Shutdown Dispatcher %s is not alive' \
                                     % process)
                    self.shutdown()
                    
    def shutdown(self):
        self.exit.set()
                
    def run(self):
            self.__setup()
            self.__start()
            while not self.exit.is_set():
                self.__monitor()
                try:
                    self.__queueupdate(self.queue.get_nowait())
                except:
                    pass
                sleep(5)

