from datetime import datetime

from . import db
from .user import User


class Message(db.Document):
    sender_id = db.ReferenceField(User, required=True, null=False)
    receiver_id = db.ReferenceField(User, required=True, null=False)
    message_body = db.BinaryField(required=True, null=False)
    created_at = db.DateTimeField(null=False, required=True, default=datetime.utcnow)
    forwarded_at = db.DateTimeField(default=None)

    def __str__(self):
        return f'<MESSAGE TO FORWARD: PK={self.pk}, SENDER={self.sender_id}, RECEIVER={self.receiver_id}, ' \
               f'MESSAGE={self.message_body}>'

    @staticmethod
    def get_connections(user_id):
        pipeline = [
            {"$match": {"$or": [{"sender_id": user_id}, {"receiver_id": user_id}]}},
            {"$project": ""}
        ]
        Message.objects().aggregate(pipeline)

    @staticmethod
    def get_chat_history(user_id1, user_id2):
        pipeline = [
            {
                "$match": {
                    "$or": [
                        {"$and": [{"sender_id": user_id1}, {"receiver_id": user_id2}]},
                        {"$and": [{"sender_id": user_id2}, {"receiver_id": user_id1}]}
                    ]
                }
            },
            {"$sort": {"created_at": 1}}
        ]
        messages = Message.objects().aggregate(pipeline)
        return messages

    @staticmethod
    def get_unreceived_messages(user_id):
        pipeline = [
            {"$match": {"receiver_id": user_id, "forwarded_at": None}},
            {"$sort": {"created_at": 1}},
            {
                "$group": {
                    "_id": {"sender_id": "$sender_id"},
                    "count": {"$sum": 1},
                }
            }
        ]
        messages = Message.objects().aggregate(pipeline)
        return messages
