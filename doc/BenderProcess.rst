``BenderProcess``
======================

.. automodule:: BenderBot.BenderProcess
    :members:
    
    BenderProcess was designed to be subclassed for your IRC process needs,
    I'll give an example below::
    
        $ ls -l
        total 8
        drwxr-xr-x  6 jeffreyness  staff  204 Sep 10 10:06 BenderBot_Time
        drwxr-xr-x  8 jeffreyness  staff  272 Sep 10 10:06 BenderBot_Time.egg-info
        drwxr-xr-x  3 jeffreyness  staff  102 Sep 10 10:06 config
        -rw-r--r--  1 jeffreyness  staff  564 Sep 10 10:04 setup.py
        
    The module we use will be ``BenderBot_Time.Time``::
    
        $ cat BenderBot_Time/Time.py
        from BenderBot.BenderProcess import BenderProcess
        from time import sleep, time
                
        class WhatTime(BenderProcess):
        
            def run(self):
                while True:
                    self.irc.sendchannel(time())
                    sleep(10)
                            
    As long as this class is importable we can put it right in our configuration::
    
        $ cat config/bender.conf-example 
        # This configuration should be appened to
        # your ~/.bender.conf file along with BenderBot's
        # configuration.
        #
        # This plugin is meant to replace IRCProcess
        # or any other IRC process that handles
        # readsocket.
        #
        [TimeProcess]
        library = BenderBot_Time.Time
        class = WhatTime
        
        # If a important process dies the entire bot will die
        important = False
        
        # This process requires access to the IRC message queue
        listen = False
        
    We can now run **Bender** and see our new process being ran every 10 seconds::
    
        $ Bender 
        2012-09-10 10:06:48,341 - INFO - Starting IRCProcess
        2012-09-10 10:06:48,341 - INFO - connecting to 10.1.184.178:6667
        2012-09-10 10:06:48,342 - INFO - setting nick to benderbot
        2012-09-10 10:06:50,350 - INFO - joining channel #bender-test
        2012-09-10 10:06:50,352 - INFO - Starting Dispatcher
        2012-09-10 10:06:50,375 - INFO - Starting process HTTPListenerProcess
        2012-09-10 10:06:50,421 - INFO - Starting process TimeProcess
        2012-09-10 10:06:50,426 - INFO - sending: PRIVMSG #bender-test :1347289610.43
        2012-09-10 10:07:00,423 - INFO - sending: PRIVMSG #bender-test :1347289620.42

