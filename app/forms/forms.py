from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreatFormLink(Form):
    name = StringField('name', [DataRequired()])
    submit = SubmitField('Creat')
