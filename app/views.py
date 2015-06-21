import datetime
from app import app, db, lm, cache
from models import User, Word
from forms import WordForm
from oauth import OAuthSignIn
from flask import request, render_template, redirect, url_for, \
    render_template, g, flash, jsonify
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from sqlalchemy import and_

@app.route('/')
@app.route('/today')
@login_required
@cache.cached(timeout=120)
def today():
    return render_template('today.html',
                           title='Today')

@lm.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))

@app.route('/login')
@cache.cached(timeout=120)
def login():
    if current_user.is_authenticated():
        return redirect(url_for('today'))

    return render_template('login.html',
                           title='Login')

@app.route('/list')
@login_required
@cache.cached(timeout=120)
def list():
    WORDS_PER_PAGE = app.config['WORDS_PER_PAGE']
    return render_template('list.html',
                           title='List',
                           WORDS_PER_PAGE=WORDS_PER_PAGE)

@app.route('/api/list')
@login_required
def api_list():
    page_number_args = request.args.get('page_number')
    search_word_args = request.args.get('search_word')

    WORDS_PER_PAGE = app.config['WORDS_PER_PAGE']

    if page_number_args is not None:
        try:
            page_number = int(page_number_args)
        except ValueError:
            return jsonify(email=g.user.email,
                           words=[],
                           error_code=500,
                           error_msg='page_number value not valid')
    else:
        page_number = 1

    # Query builder
    query = g.user.words
    if search_word_args is not None and search_word_args != '':
        query = query.filter(Word.name.like('%' + search_word_args + '%'))

    words = query.paginate(page_number, WORDS_PER_PAGE, False).items

    return jsonify(email=g.user.email,
                   words=[word.serialize for word in words])



@app.route('/api/today')
@login_required
def api_today():
    words_today = get_today_words()

    return jsonify(words=[word.serialize for word in words_today],
                   today=datetime.date.today().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    # Receiving data
    form = WordForm()
    if form.validate_on_submit():
        word = Word(name=form.name.data,
                    explain=form.explain.data,
                    example=form.example.data,
                    created_at=datetime.datetime.utcnow(),
                    updated_at=datetime.datetime.utcnow(),
                    user_id=g.user.id)

        db.session.add(word)
        db.session.commit()
        flash('Word "%s" has been saved.' % form.name.data, 'info')
        return redirect(url_for('add'))

    return render_template('form.html',
                           form=form,
                           title='Add')

@app.route('/edit/<int:word_id>', methods=['GET', 'POST'])
@login_required
def edit(word_id):
    word = Word.query.filter_by(id=word_id).first()

    if word == None:
        flash('Word not found. Add a word!', 'info')
        return redirect(url_for('add'))
    elif word.user_id != g.user.id:
        flash('You can\'t edit this word!', 'warning')
        return redirect(url_for('add'))

    form = WordForm(obj=word)
    if form.validate_on_submit():
        word.name = form.name.data
        word.explain = form.explain.data
        word.example = form.example.data
        word.updated_at = datetime.datetime.utcnow()
        db.session.add(word)
        db.session.commit()

    flash('Word "%s" has been modified.' % form.name.data, 'info')
    return render_template('form.html',
                           form=form,
                           title='Edit',
                           word=word.name)

@app.route('/delete/<int:word_id>', methods=['DELETE'])
@login_required
def delete(word_id):
    word = Word.query.filter_by(id=word_id).first()

    if word == None:
        return jsonify(status=302,
                       message=('Word not found.'))
    elif word.user_id != g.user.id:
        return jsonify(status=401,
                       message=('You can\'t delete this word!'))
    else:
        db.session.delete(word)
        db.session.commit()

    return jsonify(status=200,
                   message=('word %s deleted' % word.id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('today'))

    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('today'))

    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)

    return redirect(url_for('today'))

@app.before_request
def before_request():
    g.user = current_user

# private function, get today's words list
def get_today_words(user = None):
    day_delta = app.config['DAY_DELTA']
    words_today = []

    if user is not None:
        current_user = user
    else:
        current_user = g.user
    for repeat_count in xrange(len(day_delta)):
        interval = {
            'left':  datetime.date.today() -\
                     datetime.timedelta(days=day_delta[repeat_count]),
            'right': datetime.date.today() -\
                     datetime.timedelta(days=day_delta[repeat_count] - 1),
        }
        words = db.session.query(Word).filter(
            and_(
                Word.created_at.between(interval['left'],
                                        interval['right']),
                Word.user_id == current_user.id)
            ).all()
        words_today += words

    return words_today
