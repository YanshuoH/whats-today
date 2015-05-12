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

    LIST_AUTOLOAD_INTERVAL = 1000 * 120

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
