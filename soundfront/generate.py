import random
import time
import string

from db import Database
from user import UserRepo
from album import AlbumRepo

database = Database()
database.connect()

user_repo = UserRepo(database.conn)
album_repo = AlbumRepo(database.conn)

# create a user, and an ablum for that user
user = user_repo.create_user(
    email='mlink@ksu.edu' + str(random.random()), display_name='Matt', password='pass')
album_repo.create_album(user_id=user.UserID, album_title='The Less I Know the Better',
                        album_length='90', album_price='1', album_description='A Nice Album')


# create many users for testing pagination
# for x in range(0, 300):
#     random_string = ''.join(random.choices(
#         string.ascii_uppercase + string.digits, k=12))
#     user = user_repo.create_user(email=random_string, display_name=random_string, password='pass'
#                                  )
