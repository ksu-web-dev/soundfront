import os

from flask import Flask
from .db import Database


def create_app():
    app = Flask(__name__)

    database = Database()
    database.connect()

    @app.route('/hello')
    def hello():
        return "Hello, world!"

    @app.route('/db-test')
    def db_test():
        return database.get_version()

    return app
