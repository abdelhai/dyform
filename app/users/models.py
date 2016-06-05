from werkzeug import generate_password_hash, check_password_hash
from mongoengine import *
from config import connect_db

connect_db()


class User(Document):
    email = StringField(max_length=120, required=True, unique=True)
    username = StringField(max_length=50, unique=True)
    firstname = StringField(max_length=50)
    lastname = StringField(max_length=50)
    password = StringField(max_length=100)

    def __unicode__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email
