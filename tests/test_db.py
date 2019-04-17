import unittest
from soundfront import Database

class TestDatabase(unittest.TestCase):
    def test_connect(self):
        db = Database(database='soundfront_test', setup=True)
        db.connect()


