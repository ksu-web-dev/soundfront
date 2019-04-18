import os
import random
import time

from flask import Flask, render_template
from .db import Database
from . import auth
from .repo import UserRepo, AlbumRepo


def create_app():
    app = Flask(__name__)

    database = Database()
    database.connect()
    app.config['db'] = database
    app.config['user'] = UserRepo(database.conn)
    app.config['album'] = AlbumRepo(database.conn)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')


    app.register_blueprint(auth.bp)

    album_repo = app.config['album']
    user_repo = app.config['user']

    # create some data
    random.seed(time.time())
    user_repo.create_user(email='mlink@ksu.edu' + str(random.random()), display_name='Matt', password='pass')
    album_repo.create_album(user_id='1', album_title='The Less I Know the Better', album_length='90', album_price='1', album_description='A Nice Album')

    @app.route('/')
    def index():
        # album_repo = app.config['album']
        # user_repo = app.config['user']
        
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