import unittest
import glob
import logging
import StringIO
import os.path
from user import User
from user import Professor
from user import Student
from question import Question

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

    def tearDown(self):
        # user_key = list(User.query(User.user_name == self.user.user_name))
        # for user in user_key:
        #     user.key.delete()
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
        self.assertIsFalse(User(first_name="first", last_name="last", user_name="user", password=""))

    def test_set_username(self):
        self.user.username = 'Kyle'
        self.assertEqual(self.user.username, 'Kyle')

    def test_set_password(self):
        self.user.password = 'kylesuckslol'
        self.assertEqual(self.user.password, 'kylesuckslol')

    def test_unique_user_names(self):
        self.assertFalse(User(first_name="first", last_name="last", user_name="user", password=""))

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

class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student(first_name="first", last_name="last", user_name="user", password="123")

    def tearDown(self):
        # student_key = list(Student.query(Student.user_name == self.student.user_name))
        # for user in student_key:
        #     user.key.delete()
        pass

class TestQuestion(unittest.TestCase):
    def setUp(self):
        # put some stuff in database to tie question objects to
        student_key = Student(username='student', password='password').put()
        prof_key = Professor(username='professor', password='password').put()

    def tearDown(self):
        self.student_key.delete()
        self.prof_key.delete()

    def test_post_FAQ(self):
        self.faq_as_student = Question(isFAQ=True, question='?', answer="aaaaaaa", UserObj=self.student)
        self.faq_as_admin = Question(isFAQ=True, question='???', answer="BbBbBb", UserObj=self.admin)
        self.assertFalse(self.faq_as_student.isFAQ)
        self.assertTrue(self.faq_as_admin.isFAQ)
        self.assertEqual('?', self.faq_as_student.question)
        self.assertEqual('???', self.faq_as_admin.question)
        self.assertEqual('aaaaaaa', self.faq_as_student.answer)
        self.assertEqual('BbBbBb', self.faq_as_admin.answer)
        del self.faq_as_student
        del self.faq_as_admin

    def test_set_FAQ(self):
        self.faq_as_student = Question(isFAQ=False, question='?', answer="answer", UserObj=self.student)
        self.faq_as_admin = Question(isFAQ=False, question='???', answer="ANSWER", UserObj=self.admin)
        self.assertFalse(self.faq_as_student.isFAQ)
        self.assertFalse(self.faq_as_admin.isFAQ)
        self.faq_as_student.set_FAQ(isFAQ=True)  # , self.faq_as_student
        self.faq_as_admin.set_FAQ(isFAQ=True)  # , self.faq_as_admin
        self.assertFalse(self.faq_as_student.isFAQ)
        self.assertTrue(self.faq_as_admin.isFAQ)
        del self.faq_as_student
        del self.faq_as_admin

    def test_set_answer(self):
        self.faq_as_student = Question(isFAQ=False, question='?', answer="answer", UserObj=self.student)
        self.faq_as_admin = Question(isFAQ=False, question='???', answer="ANSWER", UserObj=self.admin)
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

    def test_check_linked_list_functionality(self):
        pass

    def test_check_date(self):
        pass

    def test_empty_question(self):
        pass

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
        self.assertRaises(Student(first_name="first", last_name="last", user_name="user", password=""))

    def test_empty_username(self):
        self.assertRaises(Student(first_name="first", last_name="last", user_name="", password="123"))

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

    # to be implements next sprint?
    def test_get_questions(self):
        self.assertIsNotNone(self.student.get_all_questions())

    def test_get_unseen_questions(self):
        self.assertIsNotNone(self.student.get_all_unseen_questions())

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
        professor2 = Professor(first_name="first", last_name="last", user_name="professor", password="")
        self.assertIsNone(professor2)
        professor2.key.delete()

    def test_change_password(self):
        self.professor.change_password("234")
        self.assertTrue(self.professor.password, "234")

    def test_change_blank_password(self):
        self.assertFalse(self.professor.change_password(""))
        self.assertTrue(self.professor.password, "123")

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
        Question(isFAQ=False, question="question").put()
        self.assertIsNotNone(self.professor.load_queue())


# Class to test all the tests
class TestTests():
    test_results = []
    my_stream = StringIO.StringIO()
    list_results = []
    list_results_all = []

    test_classes_to_run = [TestSessions, TestUser, TestQuestion, TestStudent, TestProfessor]


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

