from flask import jsonify, request, current_app
from flask_migrate import Migrate

import datetime
import jwt

from app import app, db
from app.models import User, user_share_schema, users_share_schema
from app.authenticate import jwt_required


# Migrate(app, db)
#
#
app_ctx = app.app_context()
app_ctx.push()
current_app.name


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User)


# Register route
@app.route('/auth/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    result = user_share_schema.dump(
        db.session.query(User).filter_by(email=email).first()
    )
    return jsonify(result)


# Login Route
@app.route('/auth/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first_or_404()  # Return User or 404 error.

    if not user.verify_password(password):
        return jsonify({'message': 'Wrong credentials'}), 403

    #  Payload vai ser trafegado via token, com um tempo de expiração
    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10) #  Tempo exp token
    }

    #  Gerando o token de acesso
    token = jwt.encode(payload, app.config['SECRET_KEY'])

    return jsonify({'token': token.decode('utf-8')})


@app.route('/auth/protected')
@jwt_required
def protected():
    users = User.qury.all()

    return jsonify(users)
