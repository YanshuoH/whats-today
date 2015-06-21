from app import app, views, db, mail, models
from flask.ext.mail import Mail, Message

def run():
    for user in getUserList():
        words = getWordList(user)

        if len(words) > 0:
            body = getTemplate(user.nickname, \
                              getWordList(user))
            send(user.email, body)

    return True

def send(email, body):
    with app.app_context():
      global mail
      msg = Message(
                'What\'s today ?',
             sender='whats.today.words@gmail.com',
             recipients=
                 [email])
      msg.html = body
      mail.send(msg)

def getUserList():
    return models.User.query.all()

def getWordList(user):
    return views.get_today_words(user);

def getTemplate(username, words):
    return getTemplateHeader(username) + \
           getTemplateBody(words) + \
           getTemplateFooter()

def getTemplateHeader(username):
    return '<p>Dear %s:</p><br>' % username

def getTemplateFooter():
    return '<br><p>What\'s today team</p>'

def getTemplateBody(words):
    body = '<p>You have %d words \
            waiting to be reviewed today</p>' % len(words)
    body += '<ul>'
    for word in words[0:10]:
        body += '<li>%s</li>' % word.name

    body +='<li>...</li>'
    body += '</ul>'

    body += '<p><a href="%s">So, log on now!</a></p>' % app.config['APP_DOMAIN']

    return body

# Launcher
mail = Mail(app)
run()