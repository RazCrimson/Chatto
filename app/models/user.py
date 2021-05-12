import datetime

from flask_bcrypt import generate_password_hash, check_password_hash

from . import db


class User(db.Document):
    """
    User Model
    """
    username = db.StringField(unique=True, required=True, null=False, max_length=30)
    hashed_password = db.StringField(required=True, null=False)
    created_at = db.DateTimeField(null=False, default=datetime.datetime.utcnow)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password).decode('utf-8')

    def check_password(self, password) -> bool:
        return check_password_hash(self.hashed_password, password)

    def get_mongo_id(self) -> str:
        return str(self.pk)

    def __str__(self):
        return f'<USER: {self.pk}>'
