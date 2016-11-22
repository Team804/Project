import unittest
from panthertaleslol.main import User


class TestRegisterUsers(unittest.TestCase):
    def setUp(self):
        self.user = User()
		

    def tearDown(self):
        self.user.delete()

    def test_null_file(self):
		parse_info(self, input_list="")
		users = User.query.fetch()
		assertIsNone(users)

	def test_professor(self):
		self.user = Professor(first_name="Jayson", last_name="Rock", user_name="ROCK32", password="password")
		self.assertEqual(self.user.first_name, "Jayson")
		self.assertEqual(self.user.last_name, "Rock")
		self.assertEqual(self.user.user_name, "ROCK32")
		self.assertEqual(self.user.password, "password")
		self.assertIsInstance(self.user, Professor)
		self.assertIsInstance(self.user, User)
		
	def test_student(self):
		self.user = Student(first_name="Alex", last_name="Weber", user_name="WEBER68", password="")
		self.user.password = self.user.key()
		self.assertEqual(self.user.first_name, "Alex")
		self.assertEqual(self.user.last_name, "Weber")
		self.assertEqual(self.user.user_name, "WEBER68")
		self.assertEqual(self.user.password, "password")
		self.assertIsInstance(self.user, Student)
		self.assertIsInstance(self.user, User)

    def test_no_input(self):
        parse_info(self, input_list="")
		users = User.query.fetch()
		assertIsNone(users)

    def test_create_one_user(self):
        parse_info(self, input_list="kyle, vandaalwyk, VANDA24, Student")
		users = User.query.fetch()
		assertIsNotNone(users)
		assertEqual(len(users), 1)
		assertEqual(users[0].first_name, "kyle")
		assertEqual(users[0].last_name, "vandaalwyk")
		assertEqual(users[0].user_name, "VANDA24")
		assertEqual(users[0].password, "password")

    def test_create_two_users(self):
	    parse_info(self, input_list="kyle, vandaalwyk, VANDA24, Student\njen, fox, FOX36, Student")
		users = User.query.fetch()
		assertIsNotNone(users)
		assertEqual(len(users), 2)
		assertEqual(users[0].first_name, "kyle")
		assertEqual(users[0].last_name, "vandaalwyk")
		assertEqual(users[0].user_name, "VANDA24")
		assertEqual(users[0].password, "password")
		assertEqual(users[1].first_name, "jen")
		assertEqual(users[1].last_name, "fox")
		assertEqual(users[1].user_name, "FOX36")
		assertEqual(users[1].password, users[1].key())

    def test_create_same_name_users(self):
	    parse_info(self, input_list="kyle, vandaalwyk, VANDA24, Student\nkyle, vandaalwyk, FOX36, Student")
		users = User.query.fetch()
		assertIsNotNone(users)
		assertEqual(len(users), 2)
		assertEqual(users[0].first_name, "kyle")
		assertEqual(users[0].last_name, "vandaalwyk")
		assertEqual(users[0].user_name, "VANDA24")
		assertEqual(users[0].password, "password")
		assertEqual(users[1].first_name, "kyle")
		assertEqual(users[1].last_name, "vandaalwyk")
		assertEqual(users[1].user_name, "FOX36")
		assertEqual(users[1].password, "password2")

    def test_user_exists(self):
        pass

    def test_all_users_exist(self):
        pass

    # tests username, first name, last name, password, type fields
    def test_user_datastore_objects(self):
        pass



suite = unittest.TestLoader().loadTestsFromTestCase(TestRegisterUsers)
unittest.TextTestRunner(verbosity=2).run(suite)
