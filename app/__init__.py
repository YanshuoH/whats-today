import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.script import Manager
from flask.ext.cache import Cache
from flask.ext.mail import Mail
from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader

app = Flask(__name__)

# ENV configuration
env = os.environ.get('WHATSTODAY_ENV', 'dev')
app.config.from_object('app.settings.%sConfig' % env.capitalize())
app.config['ENV'] = env

# Memcached
if env == 'dev':
    # Use Simple Cache
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})
else:
    import pylibmc
    def pylibmc_cache(app, config, args, kwargs):
        return pylibmc.Client(servers=app.config['CACHE_MEMCACHED_SERVERS'],
                              binary=True)
    cache = Cache(app, config={'CACHE_TYPE': pylibmc_cache})

cache.init_app(app)

# DB
db = SQLAlchemy(app)

# Login manager
lm = LoginManager()
lm.init_app(app)

# Assets
import assets
assets_env = Environment(app)
assets_loader = PythonAssetsLoader(assets)
for name, bundle in assets_loader.load_bundles().iteritems():
    assets_env.register(name, bundle)

# Script manager
manager = Manager(app)

mail = Mail()
# Mail manager
mail.init_app(app)

from app import views, models
