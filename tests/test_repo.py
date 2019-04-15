import unittest
from soundfront.db import Database
from soundfront.repo import UserRepo


class TestRepo(unittest.TestCase):
    def setUp(self):
        self.db = Database(database='soundfront_test')
        self.db.connect()
        self.user_repo = UserRepo(self.db.conn)

    def test_create_user(self):
        user = self.user_repo.create_user()
        self.assertEqual(user.UserID, 1)

    def test_get_user(self):
        created_user = self.user_repo.create_user(
            email='email', display_name='user', password='test')
        user = self.user_repo.get_user(created_user.UserID)
        self.assertEqual(user.UserID, created_user.UserID)

    def tearDown(self):
        self.db.destroy()
