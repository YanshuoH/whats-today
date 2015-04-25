from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired

class WordForm(Form):
    name = TextField('name', validators=[DataRequired()])
    explain = TextAreaField('explain', validators=[DataRequired()])
    example = TextAreaField('example', validators=[DataRequired()])
