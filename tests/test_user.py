import unittest
from soundfront.db import Database
from soundfront.user import UserRepo


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db = Database(database=f'soundfront_test', setup=True)
        cls.db = db
        db.connect()
        cls.user_repo = UserRepo(db.conn)

    def test_create_user(self):
        user = TestUser.user_repo.create_user(
            email='email', display_name='user', password='test')
        self.assertEqual(user.UserID, 1)

    def test_get_user(self):
        created_user = TestUser.user_repo.create_user(
            email='email2', display_name='user2', password='test')
        user = TestUser.user_repo.get_user(created_user.UserID)
        self.assertEqual(user.UserID, created_user.UserID)

    def test_list_users(self):
        users = TestUser.user_repo.list_users(1, 10)

        self.assertEqual(len(users), 2)

    def test_user_count(self):
        count = TestUser.user_repo.user_count()
        self.assertEqual(count, 2)

    def test_get_user_by_email(self):
        user = TestUser.user_repo.get_user_by_email('email')
        assert user is not None
        self.assertEqual(user.Email, 'email')

    def test_list_songs(self):
        user = TestUser.user_repo.get_user_by_email('email')
        songs = TestUser.user_repo.list_songs(user.UserID)
        self.assertEqual(len(songs), 1)

