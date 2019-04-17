import unittest
from soundfront import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(database='soundfront_test')
        self.db.connect()

    def test_destroy(self):
        self.db.destroy()



