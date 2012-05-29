.. BenderBot: A configurable bare bone IRC bot written in Python
   sphinx-quickstart on Thu May 24 15:00:01 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BenderBot's documentation!
=====================================

BenderBot is A configurable bare bone IRC bot written in Python.

The software is Open Source using the GPLv3 License and can be
downloaded from https://github.com/jness/BenderBot

We provide a number of useful IRC methods by means of a IRC class,
we also give examples of written a process driven IRC bot in ``examples/Bender.py``

Out of the box BenderBot uses the configuration to run a installed Python
module and return the results to the IRC channel. We can also write
a custom python library to read in a IRC message, and return a message.

In our example configuration we import ``os`` and run ``getcwd``
every 60 seconds with in the **ExternalProcess** section.

We also import the example library ``examples.mrbender`` and run ``listen``
in our **IRCProcess** loop::

    $ cat config/bender.conf-example 
    ....
    [IRCProcess]
    # The IRC process is responsible for reading from the network
    # socket, this mean the messages can be passed to a python function.
    #
    # The python function should take in a response message, and
    # return a response message.
    #
    # Below are some examples of IRC messages:
    #
    ## channel message format:
    # :python-benderbot!~jeffrey@127.0.0.1 PRIVMSG #bender-test :hello Bender
    #
    ## direct message format:
    # :nessy!~jeffrey@127.0.0.1 PRIVMSG python-benderbot :hey
    #
    library = examples.mrbender
    function = listen
    
    [ExternalProcess]
    # An external process in BenderBot for running a custom
    # python function, the example below will use the os module
    # to then run getcwd() and send the
    # results to the IRC channel every 60 seconds.
    library = os
    function = getcwd
    interval = 60
    
With this configuration in place, and the BenderBot Python module being installed
we can run the ``Bender`` command::

    $ Bender 
    2012-05-29 12:26:29,066 - INFO - connecting to irc.freenode.net:6667
    2012-05-29 12:26:29,204 - INFO - setting nick to python-benderbot
    2012-05-29 12:26:39,205 - INFO - joining channel #bender-test
    2012-05-29 12:26:39,216 - INFO - sending: PRIVMSG #bender-test :/Users/jeffreyness/Python/BenderBot
    2012-05-29 12:27:16,799 - INFO - sending: PRIVMSG #bender-test :Hello meatbag!

And from an IRC client a user would see something like so::

    12:26 -!- python-benderbot [~python-be@127.0.0.1] has joined #bender-test
    12:26 < python-benderbot> /Users/jeffreyness/Python/BenderBot
    12:27 < nessy> hi bender
    12:27 < python-benderbot> Hello meatbag!
    
Or write you own using ``examples/Bender.py`` as a reference!

Contents:

.. toctree::
   :maxdepth: 2
   
   IRC
   Configuration
   Logger



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

