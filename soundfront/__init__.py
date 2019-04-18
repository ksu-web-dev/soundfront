import os

from flask import Flask, render_template
from .db import Database

from .auth  import bp as auth_bp
from .index import bp as index_bp
from .album import bp as album_bp, AlbumRepo
from .user  import UserRepo


def create_app():
    app = Flask(__name__)

    database = Database()
    database.connect()
    app.config['db'] = database
    app.config['user'] = UserRepo(database.conn)
    app.config['album'] = AlbumRepo(database.conn)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

    app.register_blueprint(auth_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(album_bp)

    @app.route('/hello')
    def hello():
        return "Hello, world!"

    @app.route('/db-test')
    def db_test():
        return database.get_version()

    return app