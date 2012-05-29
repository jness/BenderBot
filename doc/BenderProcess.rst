``BenderProcess``
======================

.. automodule:: BenderBot.BenderProcess
    :members:
    
    BenderProcess was designed to be subclassed for your IRC process needs,
    I'll give an example below::
    
        $ cat subclass/whattimeisit.py 
        from BenderBot.BenderProcess import BenderProcess
        from time import sleep, time
        
        class WhatTime(BenderProcess):
        
            def run(self):
                while True:
                    self.irc.sendchannel(time())
                    sleep(10)
                    
    As long as this class is importable we can put it right in our configuration::
    
        $ cat ~/.bender.conf
        ...
        [Process2]
        library = subclass.whattimeisit
        class = WhatTime
        
    We can now run Bender and see our new process being ran every 10 seconds::
    
        $ Bender 
        2012-05-29 17:54:41,052 - INFO - connecting to irc.freenode.net:6667
        2012-05-29 17:54:41,194 - INFO - setting nick to python-benderbot
        2012-05-29 17:54:51,195 - INFO - joining channel #bender-test
        2012-05-29 17:54:51,195 - INFO - Starting process Process1
        2012-05-29 17:54:51,204 - INFO - Starting process Process2
        2012-05-29 17:54:51,208 - INFO - sending: PRIVMSG #bender-test :1338332091.21
        2012-05-29 17:55:01,210 - INFO - sending: PRIVMSG #bender-test :1338332101.21
        2012-05-29 17:55:11,211 - INFO - sending: PRIVMSG #bender-test :1338332111.21

