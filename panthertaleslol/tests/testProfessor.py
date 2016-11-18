import unittest
from panthertaleslol.user import Professor

class TestProfessor(unittest.TestCase):
    def setUp(self):
        self.prof_key = Professor()

    def tearDown(self):
        self.prof_key.delete()





suite = unittest.TestLoader().loadTestsFromTestCase(TestProfessor)
unittest.TextTestRunner(verbosity=2).run(suite)
