import unittest
from panthertaleslol.user import Student

class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student_key = Student()

    def tearDown(self):
        self.student_key.delete()




suite = unittest.TestLoader().loadTestsFromTestCase(TestStudent)
unittest.TextTestRunner(verbosity=2).run(suite)
