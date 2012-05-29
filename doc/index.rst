.. BenderBot: A configurable bare bone IRC bot written in Python
   sphinx-quickstart on Thu May 24 15:00:01 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BenderBot's documentation!
=====================================

BenderBot is A configurable bare bone IRC bot written in Python.

We provide a number of useful IRC methods by means of a IRC class,
we also give examples of written a process driven IRC bot in ``examples/Bender.py``

Out of the box BenderBot uses the configuration to run a installed Python
module and return the results to the IRC channel.

In our example configuration we import ``datetime`` and run ``datetime.datetime.now().ctime()``
every 30 seconds with in the **ExternalProcess** section::

    $ cat config/bender.conf-example 
    ....
    [ExternalProcess]
    # An external process in BenderBot for running a custom
    # python function, the example below will use the datetime module
    # to then run datetime.datetime.now().ctime() and send the
    # results to the IRC channel every 30 seconds.
    module = datetime
    function = datetime.now().ctime()
    interval = 30
    
With this configuration in place, and the BenderBot Python module being installed
we can run the ``Bender`` command::

    $ Bender 
    2012-05-25 15:32:34,469 - INFO - connecting to irc.freenode.net:6667
    2012-05-25 15:32:34,608 - INFO - setting nick to BenderBot
    2012-05-25 15:32:44,609 - INFO - joining channel #bender-test
    2012-05-25 15:32:44,625 - INFO - sent "Fri May 25 15:32:44 2012" to channel
    2012-05-25 15:33:14,627 - INFO - sent "Fri May 25 15:33:14 2012" to channel
    2012-05-25 15:33:44,628 - INFO - sent "Fri May 25 15:33:44 2012" to channel
    2012-05-25 15:34:14,630 - INFO - sent "Fri May 25 15:34:14 2012" to channel

And from an IRC client a user would see something like so::

    15:32 -!- BenderBot [~BenderBot@127.0.0.1] has joined #bender-test
    15:32 < BenderBot> Fri May 25 15:32:44 2012
    15:33 < BenderBot> Fri May 25 15:33:14 2012
    15:33 < BenderBot> Fri May 25 15:33:44 2012
    15:34 < BenderBot> Fri May 25 15:34:14 2012
    
If you simply need a IRC Bot that runs a script every **X** seconds,
all you need to do is make a python module and reference it in ``~/.bender.conf``.
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

