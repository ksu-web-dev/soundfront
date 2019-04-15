import unittest
from soundfront import Database

class TestDatabase(unittest.TestCase):
    def test_connect(self):
        self.db = Database(database='soundfront_test')
        self.db.connect()

    def tearDown(self):
        self.db.destroy()



