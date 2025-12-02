import configparser
import os.path


def load_config():
    cfg=configparser.ConfigParser()
    path=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','config','config.ini'))
    cfg.read(path)
    return cfg

config=load_config()