from app import app
from models import User
from oauth import OAuthSignIn
from flask import render_template
from flask.ext.login import login_user, logout_user, current_user, \
    login_required


@app.route('/')
def index():
    return render_template('login.html',
                           title='Login')

@app.route('/main')
def main():
    return render_template('main.html',
                           title='Main')

@app.route('/list')
def list():
    return render_template('list.html',
                           title='List')

@app.route('/today')
def today():
    return render_template('today.html',
                           title='Today')

@app.route('/edit')
def edit():
    return render_template('form.html',
                           title='Edit')

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('main'))