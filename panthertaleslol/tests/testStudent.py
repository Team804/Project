import unittest
from panthertaleslol.user import Student
# from google.appengine.api import memcache
# from google.appengine.ext import ndb
# from google.appengine.ext import testbed

class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student(first_name="first", last_name="last", user_name="user", password="123")

    def tearDown(self):
        student = Student.query(Student.first_name==self.student.first_name).fetch()
        if student:
            student.key.delete()

    def test_user_not_null(self):
        self.assertNotEqual(None, self.student)

    def test_empty_first_name(self):
        student = Student(first_name="", last_name="last", user_name="user", password="123")
        self.assertIsNotNone(student)
        student.key.delete()

    def test_empty_last_name(self):
        student = Student(first_name="first", last_name="", user_name="user", password="123")
        self.assertIsNotNone(student)
        student.key.delete()

    def test_empty_password(self):
        student = Student(first_name="first", last_name="last", user_name="user", password="")
        self.assertIsNone(student)
        student.key.delete()

    def test_set_username(self):
        self.student.username = 'Kyle'
        self.assertEqual(self.student.username, 'Kyle')

    def test_set_password(self):
        self.student.password = 'kylesuckslol'
        self.assertEqual(self.student.password, 'kylesuckslol')

    def test_unique_user_names(self):
        student2 = Student(first_name="first", last_name="last", user_name="user", password="")
        self.assertIsNone(student2)
        student2.key.delete()

    def test_change_password(self):
        self.student.change_password("234")
        self.assertTrue(self.student.password, "234")

    def test_change_blank_password(self):
        self.assertFalse(self.student.change_password(""))
        self.assertTrue(self.student.password, "123")

    def test_change_blank_password(self):
        self.assertFalse(self.student.change_password(""))
        self.assertTrue(self.student.password, "123")

    def test_change_short_password(self):
        self.assertFalse(self.student.change_password("23"))
        self.assertTrue(self.student.password, "123")

    def test_change_no_numbers_password(self):
        self.assertFalse(self.student.change_password("badpass"))
        self.assertTrue(self.student.password, "123")

    #to be implements next sprint?
    def test_get_questions(self):

        self.assertIsNotNone(self.student.get_all_questions())

    def test_get_unseen_questions(self):
        self.assertIsNotNone(self.student.get_all_unseen_questions())

    # def setUp(self):
    #     # First, create an instance of the Testbed class.
    #     self.testbed = testbed.Testbed()
    #     # Then activate the testbed, which prepares the service stubs for use.
    #     self.testbed.activate()
    #     # Next, declare which service stubs you want to use.
    #     self.testbed.init_datastore_v3_stub()
    #     self.testbed.init_memcache_stub()
    #     # Clear ndb's in-context cache between tests.
    #     # This prevents data from leaking between tests.
    #     # Alternatively, you could disable caching by
    #     # using ndb.get_context().set_cache_policy(False)
    #     ndb.get_context().clear_cache()
    #     self.student_key = Student()
    #
    # def tearDown(self):
    #     self.student_key.delete()
    #     self.testbed.deactivate()
    #
    # def test_create_student(self):
    #     self.IsNotNone(Student())
    #
    # def test_create_student_with_fields(self):
    #     self.assertIsNotNone(Student(first_name="sam", last_name="smith", user_name="samsm1"))

suite = unittest.TestLoader().loadTestsFromTestCase(TestStudent)
unittest.TextTestRunner(verbosity=2).run(suite)
