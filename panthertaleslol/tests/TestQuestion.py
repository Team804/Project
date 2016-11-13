import unittest
from panthertaleslol.main import Question
from panthertaleslol.main import User

class TestQuestion(unittest.TestCase):
    def setUp(self):
        self.student = User(username='student', password='password', type='Student')
        self.admin = User(username='admin', password='password', type='Admin')

    def tearDown(self):
        #del self.faq_as_student
        #del self.faq_as_admin
        pass

    def test_post_FAQ(self):
        self.faq_as_student = Question(bIsFAQ=True, StrQuestion='?', answer="aaaaaaa", UserObj=self.student)
        self.faq_as_admin = Question(bIsFAQ=True, StrQuestion='???', answer="BbBbBb", UserObj=self.admin)
        self.assertFalse(self.faq_as_student.isFAQ)
        self.assertTrue(self.faq_as_admin.isFAQ)
        self.assertEqual('?', self.faq_as_student.question)
        self.assertEqual('???', self.faq_as_admin.question)
        self.assertEqual('aaaaaaa', self.faq_as_student.answer)
        self.assertEqual('BbBbBb', self.faq_as_admin.answer)
        del self.faq_as_student
        del self.faq_as_admin

    def test_set_FAQ(self):
        self.faq_as_student = Question(bIsFAQ=False, StrQuestion='?', answer="answer", UserObj=self.student)
        self.faq_as_admin = Question(bIsFAQ=False, StrQuestion='???', answer="ANSWER", UserObj=self.admin)
        self.assertFalse(self.faq_as_student.isFAQ)
        self.assertFalse(self.faq_as_admin.isFAQ)
        self.faq_as_student.set_FAQ(isFAQ=True) #, self.faq_as_student
        self.faq_as_admin.set_FAQ(isFAQ=True) #, self.faq_as_admin
        self.assertFalse(self.faq_as_student.isFAQ)
        self.assertTrue(self.faq_as_admin.isFAQ)
        del self.faq_as_student
        del self.faq_as_admin

    def test_set_answer(self):
        self.faq_as_student = Question(bIsFAQ=False, StrQuestion='?', answer="answer", UserObj=self.student)
        self.faq_as_admin = Question(bIsFAQ=False, StrQuestion='???', answer="ANSWER", UserObj=self.admin)
        self.faq_as_student.set_answer("")
        self.faq_as_admin.set_answer("   .   ")
        self.assertEqual("", self.faq_as_student.answer)
        self.assertEqual("   .   ", self.faq_as_admin)

    def test_check_linked_list_functionality(self):
        pass

    def test_check_date(self):
        pass

    def test_empty_question(self):
        pass


suite = unittest.TestLoader().loadTestsFromTestCase(TestQuestion)
unittest.TextTestRunner(verbosity=2).run(suite)

