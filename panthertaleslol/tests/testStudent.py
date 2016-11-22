import unittest
from panthertaleslol.user import Student
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class TestStudent(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()
        self.student_key = Student()

    def tearDown(self):
        self.student_key.delete()
        self.testbed.deactivate()

    def test_create_student(self):
        self.IsNotNone(Student())

    def test_create_student_with_fields(self):
        self.assertIsNotNone(Student(first_name="sam", last_name="smith", user_name="samsm1"))

suite = unittest.TestLoader().loadTestsFromTestCase(TestStudent)
unittest.TextTestRunner(verbosity=2).run(suite)
