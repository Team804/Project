import unittest
from . import main

class TestUser(unittest.TestCase):
    def setup(self):
        self.user = main.User()

    def tearDown(self):
        del self.user

    def create_user(self):
        self.assertNotNull(self.user)

    def set_username(self):
        self.user.username = 'Kyle'
        self.assertEqual(self.user.username, 'Kyle')

    def set_password(self):
        self.user.password = 'kylesuckslol'
        self.assertEqual(self.user.password, 'kylesuckslol')

    def set_type(self):
        self.user.type = 'student'
        self.assertEqual(self.user.type, 'student')

    def get_user(self):
        pass


