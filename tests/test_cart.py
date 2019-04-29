import unittest
from soundfront.db import Database
from soundfront.user import UserRepo
from soundfront.cart import CartRepo
from soundfront.song import SongRepo


class TestCart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db = Database(database=f'soundfront_cart_test', setup=True, test=True)
        cls.db = db
        db.connect()
        cls.user_repo = UserRepo(db.conn)
        cls.song_repo = SongRepo(db.conn)
        cls.cart_repo = CartRepo(db.conn)

    def test_get_cart(self):
        user = TestCart.user_repo.create_user(
            email='email', display_name='user', password='test')

        cart = TestCart.cart_repo.get_cart(user.UserID)

        self.assertEqual(cart.CartID, 1)

    def test_add_song_to_cart(self):
        song = TestCart.song_repo.insert_song(
            userid=1,
            title='some song',
            length=230,
            price=1,
            description='some description'
        )

        cart = TestCart.cart_repo.get_cart(1)

        songcart = TestCart.cart_repo.add_song_to_cart(1, 1)
