class Config(object):
    SECRET_KEY = 'secret key'

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    ASSETS_DEBUG=True