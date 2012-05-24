.. BenderBot: A configurable bare bone IRC bot written in Python
   sphinx-quickstart on Thu May 24 15:00:01 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BenderBot's documentation!
=====================================

BenderBot is A configurable bare bone IRC bot written in Python.

We provide a number of use IRC method by means of a IRC class,
and give examples of written a process driven IRC bot in ``examples/Bender.py``

Running ``examples/Bender.py`` should output you results similar to the below,
that is if you copied your configuration in place correctly::

    $ python examples/Bender.py 
    [INFO] connecting to irc.freenode.net:6667
    [INFO] setting nick to BenderBot
    [INFO] joining channel #bender-test
    [INFO] running Custom Github Process
    [INFO] received: PING :niven.freenode.net
    [INFO] received: PING :niven.freenode.net
    [INFO] running Custom Github Process

And from an IRC client a user would see something like so::

    16:43:49 *** BenderBot ~BenderBot@127.0.0.1 has joined #bender-test
    16:43:50 < BenderBot> BenderBot last pushed @ 2012-05-24T20:57:58Z
    16:48:50 < BenderBot> BenderBot last pushed @ 2012-05-24T21:47:48Z

Contents:

.. toctree::
   :maxdepth: 2
   
   IRC
   Configuration



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

