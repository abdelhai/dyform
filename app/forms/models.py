import datetime
from mongoengine import (Document, DynamicDocument,
                         DateTimeField, ReferenceField,
                         SequenceField, StringField)
from config import connect_db
from app.users.models import User

connect_db()


class FormLink(Document):
    fid = SequenceField()
    name = StringField(max_length=50)
    creator = ReferenceField(User, dbref=True)
    date_modified = DateTimeField(default=datetime.datetime.now)


class Thread(Document):
    tid = SequenceField()
    formlink = ReferenceField(FormLink, dbref=True)
    date_modified = DateTimeField(default=datetime.datetime.now)


class FormData(DynamicDocument):
    creator = ReferenceField(User, dbref=True)
    thread = ReferenceField(Thread, dbref=True)
    date_modified = DateTimeField(default=datetime.datetime.now)


class InboundData(DynamicDocument):
    date_modified = DateTimeField(default=datetime.datetime.now)
