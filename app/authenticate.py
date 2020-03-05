from functools import wraps
import jwt
from flask import request, jsonify, current_app
from app.models import User


"""
Criar um decorador que sempre vai verificar se o usuário passou o token ou não, o token garante
que o usuário esteja logado.
#  Esta biblioteca ajuda na criação de um decorador personalizado
"""


# Recebe uma função como parâmetro
def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None
        # if 'authorization' in request.headers:
        #     token = request.headers['authorization']

        if not token:
            return jsonify({'message': 'Permission Denied to access this route'}), 403

        if 'Bearer' not in token:
            return jsonify({'message': 'Invalid token'}), 401

        try:
            token_pure = token.replace("Bearer", "")
            decoded = jwt.decode(token_pure, current_app.config['SECRET_KEY'])
            current_user = User.query.get(decoded['id'])
        except:
            return jsonify({'message': 'Invalid Token'}), 403

        return f(current_user=current_user, *args, **kwargs)

    return wrapper()
