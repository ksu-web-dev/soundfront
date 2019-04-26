import os
import math

from flask import Flask, render_template
from .db import Database

from .auth import bp as auth_bp
from .index import bp as index_bp

from .album import AlbumRepo, bp as albums_bp
from .user  import UserRepo, bp as users_bp
from .song  import SongRepo, bp as songs_bp
from .tag	import TagRepo, bp as tag_bp
from .cart	import CartRepo, bp as cart_bp

def create_app():
    app = Flask(__name__)

    database = Database()
    database.connect()
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
    app.config['db'] = database
    app.config['user'] = UserRepo(database.conn)
    app.config['album'] = AlbumRepo(database.conn)
    app.config['song'] = SongRepo(database.conn)
    app.config['tag'] = TagRepo(database.conn)
    app.config['cart'] = CartRepo(database.conn)

    app.register_blueprint(auth_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(albums_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(songs_bp)
    app.register_blueprint(tag_bp)
    app.register_blueprint(cart_bp)

    @app.route('/hello')
    def hello():
        return "Hello, world!"

    @app.route('/db-test')
    def db_test():
        return database.get_version()

    app.jinja_env.filters['duration'] = format_duration
    app.jinja_env.globals.update(in_cart=in_cart)

    return app

def format_duration(duration):
    duration = int(duration)
    minutes = math.floor(duration / 60)
    seconds = duration % 60
    return f'{minutes}:{seconds:02}'

def in_cart(song_or_album, cart, type):
    for item in cart:
        if type == 'Album':
            if item.Type == 'Album' and item.ID == song_or_album.AlbumID: 
                return True
        elif type == 'Song':
            if item.Type == 'Song' and item.ID == song_or_album.SongID: 
                return True

    return False