import os

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = 'You-can-never-guess'
    WTF_CSRF_ENABLED = True

    if os.environ.get('WHATSTODAY_DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['WHATSTODAY_DATABASE_URL']
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '',
            'secret': ''
        },
    }

    DAY_DELTA = [0, 1, 2, 4, 7, 15]

    WORDS_PER_PAGE = 50

class ProdConfig(Config):
    CACHE_MEMCACHED_SERVERS = '127.0.0.1:11211'

class DevConfig(Config):
    DEBUG = True
