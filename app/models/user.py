import datetime

from . import db


class User(db.Document):
    """
    User Model
    """
    username = db.StringField(unique=True, required=True, null=False, max_length=30)
    password = db.StringField(required=True, null=False, max_length=30)
    created_at = db.DateTimeField(null=False, default=datetime.datetime.utcnow)

    def __str__(self):
        return f'<USER: {self.pk}>'
