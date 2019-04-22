import unittest
from soundfront.db import Database
from soundfront.user import UserRepo
from soundfront.song import SongRepo


class TestSong(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db = Database(database=f'soundfront_test', setup=True)
        cls.db = db
        db.connect()
        cls.user_repo = UserRepo(db.conn)
        cls.repo = SongRepo(db.conn)

    def test_insert_song(self):
        user = TestSong.user_repo.create_user(
            email='email', display_name='user', password='test')

        song = TestSong.repo.insert_song(
            userid=user.UserID,
            albumid=None,
            title='some song',
            length=230,
            price=1,
            description='some description'
        )

        self.assertEqual(song.SongID, 1)

    def test_list_song(self):
        songs = TestSong.repo.list_song(1, 10)
        self.assertEqual(len(songs), 1)
        self.assertEqual(songs[0].Title, 'some song')
