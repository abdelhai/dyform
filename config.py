import os
from mongoengine import connect
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

# set and env var:'mongodb://magnetu:<password>@<mongo host>:<port>/<db name>'
MONGODB = os.environ.get('MONGODB')

# imp also for flask-login
SECRET_KEY = os.environ.get('SECRET_KEY')

# Enpoints are not CSRF protected atm
WTF_CSRF_ENABLED = False

# SendGrid creds
SG_USER = os.environ.get('SG_USER')
SG_PASSWORD = os.environ.get('SG_PASSWORD')

# Segment.com key
SEGMENT_KEY = os.environ.get('SEGMENT_KEY')


def connect_db():
    connect('magnetdb', host=MONGODB)
