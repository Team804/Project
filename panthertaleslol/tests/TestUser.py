import unittest
from panthertaleslol.main import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def tearDown(self):
        #del self.user
        pass

    def test_create_user(self):
        self.assertNotEqual(None, self.user)

    def test_set_username(self):
        self.user.username = 'Kyle'
        self.assertEqual(self.user.username, 'Kyle')

    def test_set_password(self):
        self.user.password = 'kylesuckslol'
        self.assertEqual(self.user.password, 'kylesuckslol')

    def test_set_type(self):
        self.user.type = 'student'
        self.assertEqual(self.user.type, 'student')

    def test_get_user(self):
        pass


suite = unittest.TestLoader().loadTestsFromTestCase(TestUser)
unittest.TextTestRunner(verbosity=2).run(suite)
