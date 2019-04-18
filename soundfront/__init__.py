import os

from flask import Flask, render_template
from .db import Database
from . import auth
from .user import UserRepo


def create_app():
    app = Flask(__name__)

    database = Database()
    database.connect()
    app.config['db'] = database
    app.config['user'] = UserRepo(database.conn)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')


    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/hello')
    def hello():
        return "Hello, world!"

    @app.route('/db-test')
    def db_test():
        return database.get_version()

    return app
