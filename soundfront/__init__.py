import os

from flask import Flask, render_template
from .db import Database
from . import auth

from .user import UserRepo
from .album import AlbumRepo


def create_app():
    app = Flask(__name__)

    database = Database()
    database.connect()
    app.config['db'] = database
    app.config['user'] = UserRepo(database.conn)
    app.config['album'] = AlbumRepo(database.conn)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        album_repo = app.config['album']    
        albums = album_repo.list_albums(page=1, page_size=5)
        print(albums)
        return render_template('index.html', albums=albums)

    @app.route('/hello')
    def hello():
        return "Hello, world!"

    @app.route('/db-test')
    def db_test():
        return database.get_version()

    return app