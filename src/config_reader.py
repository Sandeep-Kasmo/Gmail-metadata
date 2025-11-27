import configparser, os

def load_config():
    cfg = configparser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), "..", "config", "config.ini")
    cfg.read(path)
    return cfg
