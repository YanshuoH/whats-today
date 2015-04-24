import os
from flask import Flask

app = Flask(__name__)

# ENV
env = os.environ.get('WHATSTODAY_ENV', 'dev')
app.config.from_object('app.settings.%sConfig' % env.capitalize())
app.config['ENV'] = env

from app import routes