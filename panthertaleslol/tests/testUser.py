import unittest
from panthertaleslol.user import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def tearDown(self):
        del self.user

    def test_user_not_null(self):
        self.assertNotEqual(None, self.user)

    def test_empty_first_name(self):
        pass

    def test_empty_last_name(self):
        pass

    def test_empty_password(self):
        pass

    def test_set_username(self):
        self.user.username = 'Kyle'
        self.assertEqual(self.user.username, 'Kyle')

    def test_set_password(self):
        self.user.password = 'kylesuckslol'
        self.assertEqual(self.user.password, 'kylesuckslol')

    def test_unique_user_names(self):
        pass

    def test_change_password(self):
        pass



suite = unittest.TestLoader().loadTestsFromTestCase(TestUser)
suite_results = unittest.TextTestRunner(verbosity=2).run(suite)
