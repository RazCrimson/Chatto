import datetime

from . import db
from .user import User


class MessageToForward(db.Document):
    sender = db.ReferenceField(User)
    receiver = db.ReferenceField(User)
    message = db.BinaryField()
    received_at = db.DateTimeField(null=False, default=datetime.datetime.utcnow)

    def __str__(self):
        return f'<MESSAGE TO FORWARD: {self.pk}>'
