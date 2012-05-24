from ConfigParser import ConfigParser
import os

def get_config():
    'Return the Configuration'
    cfg = os.path.join(os.path.dirname(os.pardir), 'config/bot.conf')
    config = ConfigParser()
    config.readfp(open(cfg))
    return config