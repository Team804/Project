import unittest
from panthertaleslol.user import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(first_name="first", last_name="last", user_name="user", password="123")

    def tearDown(self):
        pass

    def test_user_not_null(self):
        self.assertNotEqual(None, self.user)

    def test_empty_first_name(self):
        user = User(first_name="", last_name="last", user_name="user", password="123")
        self.assertIsNotNone(user)

    def test_empty_last_name(self):
        user = User(first_name="first", last_name="", user_name="user", password="123")
        self.assertIsNotNone(user)

    def test_empty_password(self):
        user = User(first_name="first", last_name="last", user_name="user", password="")
        self.assertIsNone(user)

    def test_set_username(self):
        self.user.username = 'Kyle'
        self.assertEqual(self.user.username, 'Kyle')

    def test_set_password(self):
        self.user.password = 'kylerockslol'
        self.assertEqual(self.user.password, 'kylerockslol')

    def test_unique_user_names(self):
        user2 = User(first_name="first", last_name="last", user_name="user", password="")
        self.assertIsNone(user2)

    def test_change_password(self):
        self.user.change_password("234")
        self.assertTrue(self.user.password, "234")

    def test_change_blank_password(self):
        self.assertFalse(self.user.change_password(""))
        self.assertTrue(self.user.password, "123")

    def test_change_blank_password(self):
        self.assertFalse(self.user.change_password(""))
        self.assertTrue(self.user.password, "123")

    def test_change_short_password(self):
        self.assertFalse(self.user.change_password("23"))
        self.assertTrue(self.user.password, "123")

    def test_change_no_numbers_password(self):
        self.assertFalse(self.user.change_password("badpass"))
        self.assertTrue(self.user.password, "123")


suite = unittest.TestLoader().loadTestsFromTestCase(TestUser)
suite_results = unittest.TextTestRunner(verbosity=2).run(suite)
