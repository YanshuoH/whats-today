from flask.ext.login import UserMixin

from app import app, db, lm

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

    words = db.relationship('Word', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.email)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

class Word(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(300), nullable=False)
    explain = db.Column(db.Text(), nullable=False)
    example = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Word %r>' % (self.name)

    @property
    def serialize(self):
        """return object data in easily serializeable format"""
        return {
            'id':           self.id,
            'name':         self.name,
            'explain':      self.explain,
            'example':      self.example,
            'created_at':   self.created_at.strftime("%Y-%m-%d %H:%M"),
            'updated_at':   self.updated_at.strftime("%Y-%m-%d %H:%M")
        }