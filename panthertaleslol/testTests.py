import unittest
import glob
import logging
import StringIO
import os.path
from user import User
from user import Professor

# class to test properties to be read from later in jinja template
class TestObj():
    test_class = ""
    test_result = ""
    def __init__(self, case):
        self.test_name = case


#manually add all tests in here, <3 google engine
class TestRegisterUsers(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def tearDown(self):
        pass

    def test_null_file(self):
        pass


    def test_no_input(self):
        self.assertGreater(User() is Professor)

    def test_create_one_user(self):
        pass

    def test_create_multiple_users(self):
        pass

    def test_create_same_name_users(self):
        pass

    def test_user_exists(self):
        self.assertEqual(1, 2)

    def test_all_users_exist(self):
        pass

    # tests username, first name, last name, password, type fields
    def test_user_datastore_objects(self):
        pass

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


class TestSessions(unittest.TestCase):
    def setUp(self):
        my_session = 'in_session'
        self.session['my_session'] = my_session

    def tearDown(self):
        for key in self.session:
            self.session.pop(key)
        self.assertTrue(len(self.session) == 0)

    def test_multiple_sessions(self):
        session_one = 'We '
        session_two = 'are '
        session_three = 'in '
        session_four = 'session.'

        self.session['session_one'] = session_one
        self.session['session_two'] = session_two
        self.session['session_three'] = session_three
        self.session['session_four'] = session_four

        self.assertTrue(len(self.session) == 5)
        self.assertTrue('session_one' in self.session)
        self.assertTrue('session_two' in self.session)
        self.assertTrue('session_three' in self.session)
        self.assertTrue('session_four' in self.session)
        self.assertTrue('my_session' in self.session)
        self.assertTrue(self.session['my_session'])
        self.assertTrue(self.session['session_one'])
        self.assertTrue(self.session['session_two'])
        self.assertTrue(self.session['session_three'])
        self.assertTrue(self.session['session_four'])

    def test_one_session(self):
        self.assertTrue(len(self.session) == 1)
        self.assertTrue('my_session' in self.session)
        self.assertTrue(self.session['my_session'])


# Class to test all the tests
class TestTests():
    test_results = []
    my_stream = StringIO.StringIO()
    list_results = []
    list_results_all = []
    test_classes_to_run = [TestRegisterUsers, TestUser, TestSessions]


    def run_all_tests(self):
        # current_directory = os.path.dirname(__file__)
        # parent_directory = os.path.split(current_directory)[0]
        # file_path = os.path.join(current_directory, 'testUser.py')
        # #test_files = glob.glob('test*.py') #grabs all the test files to be used
        # test_file = open(file_path)
        # test_file = test_file.read()
        # module_strings = [test_file[0:os.path.getsize(file_path) - 3] ] #for test_file in test_files
        # # print test_files
        # print module_strings
        # # logging.info(test_files)
        # suites = [unittest.defaultTestLoader.loadTestsFromName(test_file) for test_file in module_strings]
        # test_suite = unittest.TestSuite(suites)

        # ******put class names to test here*****


        loader = unittest.TestLoader()

        suites_list = []
        for test_class in self.test_classes_to_run:
            suite = loader.loadTestsFromTestCase(test_class)
            suites_list.append(suite)
        big_suite = unittest.TestSuite(suites_list)
        test_suite = unittest.TestLoader().loadTestsFromTestCase(TestUser)
        self.test_results = unittest.TextTestRunner(stream=self.my_stream, descriptions=False, verbosity=2).run(big_suite)

        # Parse output unittest is evil---> either use stream or re write test runner
        result_parse =  self.my_stream.getvalue()
        logging.info(len(result_parse))
        #self.list_results = [""]*self.test_results.testsRun
        for i in range (0, self.test_results.testsRun):
            pos = result_parse.find("...")
            pos_one = result_parse.find("(")
            test_obj = TestObj(case = result_parse[0:pos_one])
            # test suite name parse
            pos_one = result_parse.find(".")
            pos_two= result_parse.find(")")
            test_obj.test_class = result_parse[pos_one+1:pos_two]
            print test_obj.test_class
            temp_arr = result_parse[pos:len(result_parse)]


            if temp_arr.find("ok") < 5:
                pos = result_parse.find("ok")
                print result_parse[0:pos+2]
                self.list_results.append(result_parse[0:pos+2])
                test_obj.test_result = True
                result_parse = result_parse[pos+2 :len(result_parse)]
            elif temp_arr.find("E") < 5:
                pos = result_parse.find("E")
                print "ERROR"
                print result_parse[0:pos + 5]
                self.list_results.append(result_parse[0:pos + 5])
                test_obj.test_result = False
                result_parse = result_parse[pos + 5:len(result_parse)]
            else:
                pos = result_parse.find("F")
                print "FAIL"
                print result_parse[0:pos + 4]
                self.list_results.append(result_parse[0:pos + 4])
                test_obj.test_result = False
                result_parse = result_parse[pos + 4:len(result_parse)]

            self.list_results_all.append(test_obj)

if __name__ == '__main__':
    TestTests().run_all_tests()

