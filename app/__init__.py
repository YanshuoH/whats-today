import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader

app = Flask(__name__)

# ENV configuration
env = os.environ.get('WHATSTODAY_ENV', 'dev')
app.config.from_object('app.settings.%sConfig' % env.capitalize())
app.config['ENV'] = env

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


from app import views, models