import unittest
from panthertaleslol.main import BaseHandler
from panthertaleslol.main import LogoutHandler


class TestSesssions(unittest.TestCase):

    def setUp(self):
        print("Creating Session")
        my_session = 'in_session'
        self.session['my_session'] = my_session
        print("Session Created")

    def setUpMulti(self):
        print("Creating Multiple Sessions")
        session_one = 'We '
        session_two = 'are '
        session_three = 'in '
        session_four = 'session.'

        self.session['session_one'] = session_one
        self.session['session_two'] = session_two
        self.session['session_three'] = session_three
        self.session['session_four'] = session_four
        print("Sessions Created")

    def test_multiple_sessions(self):
        print('Checking for Sessions')
        self.assertTrue(len(self.session) == 4)
        print("Number of Sessions: ", len(self.session))
        print("Checking Session Contents...")
        self.assertTrue('session_one' in self.session)
        self.assertTrue('session_two' in self.session)
        self.assertTrue('session_three' in self.session)
        self.assertTrue('session_four' in self.session)
        self.assertTrue(self.session['session_one'])
        self.assertTrue(self.session['session_two'])
        self.assertTrue(self.session['session_three'])
        self.assertTrue(self.session['session_four'])
        print('Session Contents: ')
        print('Session One: ', self.session['session_one'])
        print('Session Two: ', self.session['session_two'])
        print('Session Three: ', self.session['session_three'])
        print('Session Four: ', self.session['session_four'])

    def test_session(self):
        print('Checking for Sessions')
        self.assertTrue(len(self.session) == 1)
        print("Number of Sessions: ", len(self.session))
        print("Checking Session Contents...")
        self.assertTrue('my_session' in self.session)
        self.assertTrue(self.session['my_session'])
        print('Session Contents: ', self.session['my_session'])

    def tearDown(self):
        print('Freeing All Sessions..')
        for key in self.session:
            self.session.pop(key)
        self.assertTrue(len(self.session) == 0)
        print('Sessions Freed')


suite = unittest.TestLoader().loadTestsFromTestCase(TestProfessor)
unittest.TextTestRunner(verbosity=2).run(suite)
