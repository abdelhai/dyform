from models import User
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Email, Length


class SignupForm(Form):
    email = StringField('Email:', [InputRequired(), Email()])
    username = StringField('Username', [InputRequired()])
    # firstname = StringField('firstname')
    # lastname = StringField('lasname')
    password = PasswordField('Password:',
                             [EqualTo('pw_confirm', message='Passwords must match'),
                              InputRequired(), Length(min=6)])
    pw_confirm = PasswordField('Repeat password:', [InputRequired()])
    # submit = SubmitField('Signup')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class LoginForm(Form):
    email = StringField('email', [InputRequired()])
    password = PasswordField('password')
    # submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        '''the validate function for login. the .first() is imp..
        Source: http://code.tutsplus.com/tutorials/intro-to-flask\
        -signing-in-and-out--net-29982
        '''
        if not Form.validate(self):
            return False

        user = User.objects(email=self.email.data).first()
        # check password
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False
