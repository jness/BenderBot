from ConfigParser import ConfigParser
import os

def get_config(cfg_name='~/.bender.conf'):
    '''This method will check the ``cfg_name`` for a BenderBot
    configuration file.
    
    To get started copy the ``config/bender.conf-example`` to
    ``~/.bender.conf``
    
    - **method usage**::
    
        >>> from BenderBot.Configuration import get_config
        >>> config = get_config()
        >>> config.get('IRC', 'server')
        'irc.freenode.net'
        
    '''
    cfg = os.path.expanduser(cfg_name)
    if os.path.exists(cfg):
        config = ConfigParser()
        config.readfp(open(cfg))
        return config
    else:
        raise Exception('Unable to open %s' % cfg_name)
