from flask import jsonify
from flask_migrate import Migrate

from app import app, db
from app.models import User

Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User
    )


@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    return 'Hello'


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    pass
