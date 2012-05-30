.. BenderBot: A configurable bare bone IRC bot written in Python
   sphinx-quickstart on Thu May 24 15:00:01 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BenderBot's documentation!
=====================================

BenderBot is A configurable bare bone IRC bot written in Python.

The software is Open Source and licensed under GPLv3. The source
can be viewed and downloaded from https://github.com/jness/BenderBot

We provide a number of useful IRC methods by means of the ``BenderBot.IRC`` class,
we also give examples of written a process driven IRC bot in ``examples/Bender.py``
if the current structure does not suite your needs.

BenderBot uses the configuration to connect to your IRC server, and run processes.
The processes are defined in a section within the configuration containing the word
**Process**. These processes should be subclassed from the
``BenderBot.BenderProcess.BenderProcess`` class.

Out of the box BenderBot uses the example BenderProcess to keep the bot alive,
this is thanks to ``BenderBot.IRC.readsocket`` and its ablity to PING/PONG::

    $ cat config/bender.conf-example 
    ....
    [IRCProcess]
    # Create a new process from our BenderProcess class,
    # this can easily be subclassed to do your bidding,
    # just be sure to have one process for handling IRC
    # socket reads, this keeps up PING/PONG.
    # The BenderProcess class gives an example how to handle
    # IRC readsocket (PING/PONG).
    #
    library = BenderBot.BenderProcess
    class = BenderProcess
    
With this configuration in place, and the BenderBot Python module being installed
we can run the ``Bender`` command::

    $ Bender --debug
    2012-05-29 17:42:45,608 - INFO - connecting to irc.freenode.net:6667
    2012-05-29 17:42:45,771 - INFO - setting nick to python-benderbot
    2012-05-29 17:42:55,772 - INFO - joining channel #bender-test
    2012-05-29 17:42:55,773 - INFO - Starting process IRCProcess
    2012-05-29 17:45:03,073 - DEBUG - received: PING :lindbohm.freenode.net
    2012-05-29 17:45:03,075 - DEBUG - sending: PONG :lindbohm.freenode.net
    
At the moment nothing to fancy, but that is where you come in, make Bender
do your bidding!

Contents:

.. toctree::
   :maxdepth: 2
   
   Bender
   BenderProcess
   Configuration
   IRC
   Logger



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

