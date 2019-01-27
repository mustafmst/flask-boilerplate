import datetime
import jwt

from app.main import db, flask_bcrypt
from app.main.models.blacklist import BlacklistToken
from app.main.config import key


class User(db.Model):
    """ User Model for storing user related details """
    ___tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    @property
    def password(self):
        raise AttributeError('password: write-only field')
    
    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return  flask_bcrypt.check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return "<User '{}'>".format(self.username)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes tha auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token Blacklisted. Please log again.'
            else:
                payload = jwt.decode(auth_token, key)
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log again.'
        except jwt.InvalidTokenError:
            return 'Invalid toekn. Please log again.'

