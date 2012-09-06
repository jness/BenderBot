from multiprocessing import Process, Queue
from ConfigParser import NoOptionError, NoSectionError
from importlib import import_module
from time import sleep

class Dispatcher(Process):
    ''' The Dispatcher for starting up all configured processes in
    ~/.bender.conf, '''

    def __init__(self, **kwargs):
        self.logger = kwargs.pop('logger')
        self.config = kwargs.pop('config')
        super(Dispatcher, self).__init__()
        
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
           
            # see if this process is important and needs to be watched
            self.processes.append(myclass)
            try:
                important = self.config.get(section, 'important')
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
        for p in self.important_processes:
            if not p.is_alive():
                for process in self.processes:
                    process.terminate()
                raise Exception('One of your important processes died')

        
    def run(self):
        self.__setup()
        self.__start()
        while True:
            self.__monitor()
            msg = self.queue.get()
            if msg:
                self.__queueupdate(msg)
            
