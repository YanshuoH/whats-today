import datetime
from app import app, db, lm
from models import User, Word
from forms import WordForm
from oauth import OAuthSignIn
from flask import request, render_template, redirect, url_for, \
    render_template, g, flash, jsonify
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

@app.route('/api/list')
@login_required
def api_list():
    words = g.user.words.all()
    return jsonify(email=g.user.email,
                   words=[word.serialize for word in words])

@app.route('/today')
@login_required
def today():
    return render_template('today.html',
                           title='Today')

@app.route('/edit', methods=['GET', 'POST'])
@app.route('/add', methods=['GET', 'POST'])
@login_required
def edit():
    rule = request.url_rule

    if 'edit' in rule.rule:
        title = 'Edit'
    elif 'add' in rule.rule:
        title = 'Add'

    # Receiving data
    form = WordForm()
    if form.validate_on_submit():
        print form.data
        word = Word(name=form.name.data,
                    explain=form.explain.data,
                    example=form.example.data,
                    created_at=datetime.datetime.utcnow(),
                    updated_at=datetime.datetime.utcnow(),
                    user_id=g.user.id)

        db.session.add(word)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))

    return render_template('form.html',
                           form=form,
                           title=title)

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

@app.before_request
def before_request():
    g.user = current_user