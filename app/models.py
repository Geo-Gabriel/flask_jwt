from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(84), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password, id=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User: {self.username}>"


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email")  # Password is not serialized, for security.


user_share_schema = UserSchema()  # Retorna apenas um dado serializado json
users_share_schema = UserSchema(many=True)  # Retorna varios dados serializados json
