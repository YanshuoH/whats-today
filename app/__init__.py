import os
from flask import Flask
from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader

app = Flask(__name__)

# ENV
env = os.environ.get('WHATSTODAY_ENV', 'dev')
app.config.from_object('app.settings.%sConfig' % env.capitalize())
app.config['ENV'] = env

# Assets
import assets
assets_env = Environment(app)
assets_loader = PythonAssetsLoader(assets)
for name, bundle in assets_loader.load_bundles().iteritems():
    assets_env.register(name, bundle)


from app import views