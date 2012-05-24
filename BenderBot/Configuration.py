from ConfigParser import ConfigParser
import os

def get_config():
    '''returns the configuration found in cfg_name,
    or raises an Exception'''
    cfg_name = '~/.bender.conf'
    cfg = os.path.expanduser(cfg_name)
    if os.path.exists(cfg):
        config = ConfigParser()
        config.readfp(open(cfg))
        return config
    else:
        raise Exception('Unable to open %s' % cfg_name)
