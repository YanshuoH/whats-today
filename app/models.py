from flask.ext.login import UserMixin

from app import app, db, lm

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

    # posts = db.relationship('Word', backref='user', lazy='dynamic')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

class Word(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Unicode())
    body = db.Column(db.Unicode())
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)