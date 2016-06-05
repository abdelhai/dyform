from flask import Blueprint, request, render_template, redirect, flash
from models import User
from forms import SignupForm, LoginForm
from flask_login import login_user, logout_user
import config
import analytics
analytics.write_key = config.SEGMENT_KEY

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/register/', methods=['POST', 'GET'])
def register():
    form = SignupForm()
    if request.method == 'POST' and form.validate():
        user_per_email = User.objects(email=form.email.data)
        user_per_username = User.objects(username=form.username.data)
        if user_per_email:
            form.errors['email'] = ['Email is already taken.']
        elif user_per_username:
            form.errors['username'] = ['Username is already taken.']
        else:
            user = User(email=form.email.data, username=form.username.data)
            user.set_password(form.password.data)
            user.save()
            login_user(user)
            analytics.identify(str(user.id), {'email': str(user.email)})
            analytics.track(str(user.id), 'Registered (srv)')
            return redirect('/data')

    for field, errors in form.errors.items():
        # type(errors)
        for error in errors:
            flash(u"Error in %s  - %s" % (
                getattr(form, field).label.text, error))

    return render_template('users/user.html', form=form)


@users.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.objects(email=form.email.data).first()
        login_user(user)
        analytics.identify(str(user.id), {'email': str(user.email)})
        analytics.track(str(user.id), 'Logged in (srv)')
        return redirect('/data')
    else:
        print form.errors

    return render_template('users/user.html', form=form)


@users.route('/logout/')
def logout():
    logout_user()
    return redirect('/users/login/')
