.. BenderBot: A configurable bare bone IRC bot written in Python
   sphinx-quickstart on Thu May 24 15:00:01 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BenderBot's documentation!
=====================================

BenderBot is A configurable bare bone IRC bot written in Python.

The software is Open Source and licensed under GPLv3. The source
can be viewed and downloaded from https://github.com/jness/BenderBot

We provide a number of useful IRC methods by means of the ``BenderBot.IRC`` class.

BenderBot uses the configuration to connect to your IRC server, and run processes.
The processes are defined in a section within the configuration containing the word
**Process**.

These process modules work very much like a **plugin** and should be subclassed from the
``BenderBot.BenderProcess.BenderProcess`` class.
    
With this configuration in place, and the BenderBot Python module being installed
we can run the ``Bender`` command::

    $ Bender --debug
    2012-05-29 17:42:45,608 - INFO - connecting to irc.freenode.net:6667
    2012-05-29 17:42:45,771 - INFO - setting nick to python-benderbot
    2012-05-29 17:42:55,772 - INFO - joining channel #bender-test
    2012-05-29 17:42:55,773 - INFO - Starting root IRC process
    2012-05-29 17:42:55,774 - INFO - Starting process HTTPListenerProcess
    2012-05-29 17:45:03,073 - DEBUG - received: PING :lindbohm.freenode.net
    2012-05-29 17:45:03,075 - DEBUG - sending: PONG :lindbohm.freenode.net
    
BenderBot comes with a built in API for sending messages directly to the IRC
channel by means of the IRC Bot, to use this feature be sure the HTTPListener
process is in your configuration::

    [HTTPListenerProcess]
    library = BenderBot.HTTPListener
    class = Listener
    
    # If a important process dies the entire bot will die
    important = True
    
    [HTTPListener]
    # The key used when sending HTTP POST data to the
    # http server to authorize the message.
    key = super_secret_key
    
    # The TCP address the BasicHTTPServer will bind
    # to, note this can be left blank to specify all address
    # or for security can be put to 127.0.0.1 for only local traffic.
    host = 
    
    # The TCP port BasicHTTPServer will listen on
    # for POST message
    port = 8000
    
If you copied from the example configuration you are already set,
just send some HTTP POST with appropriate JSON::

    $ curl -i -X POST -d '{"key":"super_secret_key","message":"Hello IRC Channel"}' http://127.0.0.1:8000
    HTTP/1.0 200 OK
    Server: BaseHTTP/0.3 Python/2.6.1
    Date: Thu, 28 Jun 2012 19:29:33 GMT

Using the ``curl`` command we can easily construct example POST request and
test BenderBot, in this case we sent the message ``Hello IRC Channel`` to the
channel::

    2012-06-28 14:29:33,343 - DEBUG - successfully loaded json from http post
    2012-06-28 14:29:33,343 - DEBUG - verified json object has key and message keys
    2012-06-28 14:29:33,343 - INFO - sending: PRIVMSG #bender-test :Hello IRC Channel
    
At the moment nothing to over the top fancy, this is where you come in, make Bender
do your bidding with your own plugins, or use already written plugins!

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

