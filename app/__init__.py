from flask import Flask
from app.forms.views import forms
from app.users.views import users
from flask_login import LoginManager
from users.models import User

app = Flask(__name__)
app.config.from_object('config')

# bluepronts
app.register_blueprint(forms)
app.register_blueprint(users)

# flask-login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/users/login/'


# We need a user_loader function to reload the user object through
# different sessions. This function must satisfy three conditions:
# * it takes the unicode ID of a user;
# * it returns the user object;
# * if the ID is invalid must return None.
@login_manager.user_loader
def load_user(email):
    return User.objects(email=email).first()
