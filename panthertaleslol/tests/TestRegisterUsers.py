import unittest
from panthertaleslol.main import User


class TestRegisterUsers(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def tearDown(self):
        pass

    def test_null_file(self):
        pass


    def test_no_input(self):
        pass

    def test_create_one_user(self):
        pass

    def test_create_multiple_users(self):
        pass

    def test_create_same_name_users(self):
        pass

    def test_user_exists(self):
        pass

    def test_all_users_exist(self):
        pass

    # tests username, first name, last name, password, type fields
    def test_user_datastore_objects(self):
        pass



suite = unittest.TestLoader().loadTestsFromTestCase(TestRegisterUsers)
unittest.TextTestRunner(verbosity=2).run(suite)
