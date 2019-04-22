import random
import time
import string

from db import Database
from user import UserRepo
from album import AlbumRepo

from faker import Faker
fake = Faker()

database = Database()
database.connect()

user_repo = UserRepo(database.conn)
album_repo = AlbumRepo(database.conn)

# create a user, and an ablum for that user
user = user_repo.create_user(
    email='mlink@ksu.edu' + str(random.random()), display_name='Matt', password='pass')
album_repo.create_album(user_id=user.UserID, album_title='The Less I Know the Better',
                        album_length='90', album_price='1', album_description='A Nice Album')


# create many faker users
for x in range(0, 300):
    user = user_repo.create_user(
        email=fake.email(),
        display_name=fake.name(),
        password='password'
    )
