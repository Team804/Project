import unittest
import glob
import logging
import StringIO
import os.path
from user import User
from user import Professor
from user import Student
from question import Question
import main

# class to test properties to be read from later in jinja template
class TestObj():
    test_class = ""
    test_result = ""
    def __init__(self, case):
        self.test_name = case


#manually add all tests in here, <3 google engine
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

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(first_name="first", last_name="last", user_name="user", password="123")
        self.user.put()

    def tearDown(self):
        user_keys = list(User.query(User.user_name == self.user.user_name))
        for user in user_keys:
            user.key.delete()

    def test_user_not_null(self):
        self.assertIsNotNone(self.user)

    def test_empty_first_name(self):
        user = User(first_name="", last_name="last", user_name="user", password="123")
        self.assertIsNotNone(user)

    def test_empty_last_name(self):
        user = User(first_name="first", last_name="", user_name="user", password="123")
        self.assertIsNotNone(user)

    def test_empty_password(self):
        self.assertRaises(User(first_name="first", last_name="last", user_name="user", password=""))

    def test_set_username(self):
        self.user.username = 'Kyle'
        self.assertIsNotNone(self.user)
        self.user.put()
        user = list(User.query(User.user_name == "Kyle"))[0]
        self.assertIsNotNone(user)

    def test_set_password(self):
        self.user.password = 'kylesuckslol'
        self.user.put()
        user = list(User.query(User.password == 'kylesuckslol'))[0]
        self.assertIsNot(user)

    def test_unique_user_names(self):
        self.assertRaises(User(first_name="first", last_name="last", user_name="user", password=""))

    def test_change_password(self):
        self.user.change_password("234")
        self.assertTrue(self.user.password, "234")

    def test_change_blank_password(self):
        self.assertFalse(self.user.change_password(""))
        self.assertTrue(self.user.password, "123")

    def test_change_short_password(self):
        self.assertFalse(self.user.change_password("23"))
        self.assertTrue(self.user.password, "123")

    def test_change_no_numbers_password(self):
        self.assertFalse(self.user.change_password("ba"))
        self.assertTrue(self.user.password, "123")



class TestQuestion(unittest.TestCase):
    def setUp(self):
        self.student = Student(first_name="first", last_name="last", user_name="user", password="123")

    def tearDown(self):
        # self.student_key.delete()
        # self.prof_key.delete()
        pass

    def test_post_FAQ(self):
        self.faq_as_student = Question(isFAQ=True, question='?', answer="aaaaaaa")
        self.faq_as_admin = Question(isFAQ=True, question='???', answer="BbBbBb")
        self.assertFalse(self.faq_as_student.isFAQ)
        self.assertTrue(self.faq_as_admin.isFAQ)
        self.assertEqual('?', self.faq_as_student.question)
        self.assertEqual('???', self.faq_as_admin.question)
        self.assertEqual('aaaaaaa', self.faq_as_student.answer)
        self.assertEqual('BbBbBb', self.faq_as_admin.answer)
        del self.faq_as_student
        del self.faq_as_admin

    def test_set_FAQ(self):
        self.faq_as_student = Question(isFAQ=False, question='?', answer="answer")
        self.faq_as_admin = Question(isFAQ=False, question='???', answer="ANSWER")
        self.assertFalse(self.faq_as_student.isFAQ)
        self.assertFalse(self.faq_as_admin.isFAQ)
        self.faq_as_student.set_FAQ(isFAQ=True)  # , self.faq_as_student
        self.faq_as_admin.set_FAQ(isFAQ=True)  # , self.faq_as_admin
        self.assertFalse(self.faq_as_student.isFAQ)
        self.assertTrue(self.faq_as_admin.isFAQ)
        del self.faq_as_student
        del self.faq_as_admin

    def test_set_answer(self):
        self.faq_as_student = Question(isFAQ=False, question='?', answer="answer")
        self.faq_as_admin = Question(isFAQ=False, question='???', answer="ANSWER")
        self.faq_as_student.set_answer("")
        self.faq_as_admin.set_answer("   .   ")
        self.assertEqual("", self.faq_as_student.answer)
        self.assertEqual("   .   ", self.faq_as_admin)

    def test_display_FAQ(self):
        self.faq1 = Question(isFAQ=True, question="?", answer="!")
        self.faq2 = Question(isFAQ=True, question="??", answer="!!")
        self.faq3 = Question(isFAQ=True, question="???", answer="!!!")
        self.notfaq = Question(isFAQ=False, question="!????", answer="?!!!!")
        self.assertTrue(self.faq1.isFAQ)
        self.assertTrue(self.faq2.isFAQ)
        self.assertTrue(self.faq3.isFAQ)
        self.assertFalse(self.notfaq.isFAQ)

    def test_autoset_time(self):
        pass

    def test_check_date(self):
        pass

    def test_empty_question(self):
        pass

    # to be implements next sprint?
    def test_get_questions(self):
        self.assertIsNotNone(self.student.get_all_questions())

    def test_get_unseen_questions(self):
        self.assertIsNotNone(self.student.get_all_unseen_questions())

    def test_get_url_safe_key(self):
        self.assertIsNotNone(self.student.get_all_questions()[0].get_url_safe_key())

    def test_get_question_obj_from_url_safe_key(self):
        self.assertIs(Question().get_question_from_url_safe_key(self.student.get_all_questions()[0].get_url_safe_key()))


class TestProfessor(unittest.TestCase):
    def setUp(self):
        self.professor = Professor(first_name="first", last_name="last", user_name="professor", password="123")

    def tearDown(self):
        pass

    def test_professor_not_null(self):
        self.assertNotEqual(None, self.professor)

    def test_empty_first_name(self):
        professor = Professor(first_name="", last_name="last", user_name="professor", password="123")
        self.assertIsNotNone(professor)
        professor.key.delete()

    def test_empty_last_name(self):
        professor = Professor(first_name="first", last_name="", user_name="professor", password="123")
        self.assertIsNotNone(professor)
        professor.key.delete()

    def test_empty_password(self):
        self.assertRaises(Professor(first_name="first", last_name="last", user_name="professor", password=""))

    def test_empty_professorname(self):
        self.assertRaises(Professor(first_name="first", last_name="last", user_name="", password="123"))

    def test_set_professorname(self):
        self.professor.professorname = 'Kyle'
        self.assertEqual(self.professor.professorname, 'Kyle')

    def test_set_password(self):
        self.professor.password = 'kylesuckslol'
        self.assertEqual(self.professor.password, 'kylesuckslol')

    def test_unique_user_names(self):
        professor1 = Professor(first_name="first", last_name="last", user_name="professor", password="").put()
        self.assertRaises(Professor(first_name="first", last_name="last", user_name="professor", password="").put())
        professor1.key.delete()

    def test_change_password(self):
        self.professor.change_password("234")
        self.assertTrue(self.professor.password, "234")

    def test_change_blank_password(self):
        self.assertFalse(self.professor.change_password(""))
        self.assertTrue(self.professor.password, "123")

    def test_change_short_password(self):
        self.assertFalse(self.professor.change_password("23"))
        self.assertTrue(self.professor.password, "123")

    def test_change_no_numbers_password(self):
        self.assertFalse(self.professor.change_password("badpass"))
        self.assertTrue(self.professor.password, "123")

    def test_question_queue_initially_empty(self):
        self.assertIsNone(self.professor.load_queue())

    def test_question_queue_adding(self):
        Question(isFAQ=False, question="question")
        self.assertIsNotNone(self.professor.load_queue())

class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student(first_name="first", last_name="last", user_name="user", password="123")

    def tearDown(self):
        student = Student.query(Student.first_name == self.student.first_name).fetch()
        if student:
            student.key.delete()

    def test_user_not_null(self):
        self.assertNotEqual(None, self.student)

    def test_empty_first_name(self):
        self.failUnlessRaises(Student(first_name="", last_name="last", user_name="user", password="123"))

    def test_empty_last_name(self):
        self.failUnlessRaises(first_name="first", last_name="", user_name="user", password="123")

    def test_empty_password(self):
        self.failUnlessRaises(first_name="first", last_name="last", user_name="user", password="")

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

    def test_change_short_password(self):
        self.assertFalse(self.student.change_password("23"))
        self.assertTrue(self.student.password, "123")

    def test_change_no_numbers_password(self):
        self.assertFalse(self.student.change_password("badpass"))
        self.assertTrue(self.student.password, "123")

class TestRegisterUsers(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def tearDown(self):
        self.user.delete()

    def test_null_file(self):
        main.parse_info(input_list="")
        users = User.query.fetch()
        self.assertIsNone(users)

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
        main.parse_info(input_list="")
        users = User.query.fetch()
        self.assertIsNone(users)

    def test_create_one_user(self):
        main.parse_info(input_list="kyle, vandaalwyk, VANDA24, Student")
        users = User.query.fetch()
        self.assertIsNotNone(users)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].first_name, "kyle")
        self.assertEqual(users[0].last_name, "vandaalwyk")
        self.assertEqual(users[0].user_name, "VANDA24")
        self.assertEqual(users[0].password, "password")

    def test_create_two_users(self):
        main.parse_info(input_list="kyle, vandaalwyk, VANDA24, Student\njen, fox, FOX36, Student")
        users = User.query.fetch()
        self.assertIsNotNone(users)
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].first_name, "kyle")
        self.assertEqual(users[0].last_name, "vandaalwyk")
        self.assertEqual(users[0].user_name, "VANDA24")
        self.assertEqual(users[0].password, "password")
        self.assertEqual(users[1].first_name, "jen")
        self.assertEqual(users[1].last_name, "fox")
        self.assertEqual(users[1].user_name, "FOX36")
        self.assertEqual(users[1].password, users[1].key())


    def test_create_same_name_users(self):
        main.parse_info(input_list="kyle, vandaalwyk, VANDA24, Student\nkyle, vandaalwyk, FOX36, Student")
        users = User.query.fetch()
        self.assertIsNotNone(users)
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].first_name, "kyle")
        self.assertEqual(users[0].last_name, "vandaalwyk")
        self.assertEqual(users[0].user_name, "VANDA24")
        self.assertEqual(users[0].password, "password")
        self.assertEqual(users[1].first_name, "kyle")
        self.assertEqual(users[1].last_name, "vandaalwyk")
        self.assertEqual(users[1].user_name, "FOX36")
        self.assertEqual(users[1].password, "password2")


# Class to test all the tests
class TestTests():
    test_results = []
    my_stream = StringIO.StringIO()
    list_results = []
    list_results_all = []

    test_classes_to_run = [TestSessions, TestUser, TestQuestion, TestProfessor, TestStudent]


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
        # test_suite = unittest.TestLoader().loadTestsFromTestCase(TestUser)
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
            pos_two = result_parse.find(")")
            test_obj.test_class = result_parse[pos_one+1:pos_two]
            print test_obj.test_class
            temp_arr = result_parse[pos:len(result_parse)]


            if temp_arr.find("ok") < 8 and temp_arr.find("ok") > 0:
                pos = result_parse.find("ok")
                print pos
                print result_parse[0:pos+2]
                self.list_results.append(result_parse[0:pos+2])
                test_obj.test_result = True
                result_parse = result_parse[pos+2 :len(result_parse)]
            elif temp_arr.find("ERROR") < 13 and temp_arr.find("ERROR") > 0:
                pos = result_parse.find("E")
                print "ERROR"
                print result_parse[0:pos + 5]
                self.list_results.append(result_parse[0:pos + 5])
                test_obj.test_result = False
                result_parse = result_parse[pos + 5:len(result_parse)]
            else:
                pos = result_parse.find("FAIL")
                print "FAIL"
                print result_parse[0:pos + 4]
                self.list_results.append(result_parse[0:pos + 4])
                test_obj.test_result = False
                result_parse = result_parse[pos + 4:len(result_parse)]

            self.list_results_all.append(test_obj)

if __name__ == '__main__':
    TestTests().run_all_tests()

