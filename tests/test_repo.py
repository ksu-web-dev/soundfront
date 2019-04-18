import unittest
from soundfront.db import Database
from soundfront.repo import UserRepo


class TestRepo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db = Database(database=f'soundfront_test', setup=True)
        cls.db = db
        db.connect()
        cls.user_repo = UserRepo(db.conn)

    def test_create_user(self):
        user = TestRepo.user_repo.create_user(
            email='email', display_name='user', password='test')
        self.assertEqual(user.UserID, 1)

    def test_get_user(self):
        created_user = TestRepo.user_repo.create_user(
            email='email2', display_name='user2', password='test')
        user = TestRepo.user_repo.get_user(created_user.UserID)
        self.assertEqual(user.UserID, created_user.UserID)

    def test_get_user_by_email(self):
        user = TestRepo.user_repo.get_user_by_email('email')
        assert user is not None
        self.assertEqual(user.Email, 'email')
