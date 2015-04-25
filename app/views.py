from app import app, db, lm
from models import User
from oauth import OAuthSignIn
from flask import render_template, redirect, url_for, render_template
from flask.ext.login import login_user, logout_user, current_user, \
    login_required


@app.route('/')
@login_required
def index():
    return render_template('main.html',
                           title='Main')

@lm.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html',
                           title='Login')

@app.route('/list')
@login_required
def list():
    return render_template('list.html',
                           title='List')

@app.route('/today')
@login_required
def today():
    return render_template('today.html',
                           title='Today')

@app.route('/edit')
@login_required
def edit():
    return render_template('form.html',
                           title='Edit')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

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
        return redirect(url_for('login'))

    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))