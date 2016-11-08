import unittest
from panthertaleslol.main import Question
from panthertaleslol.main import User

class TestQuestion(unittest.TestCase):
    def setup(self):
        self.student = User('student', 'password', 'Student', "")
        self.admin = User('admin', 'password', 'Admin', "")

    def tearDown(self):
        del self.faq_as_student
        del self.faq_as_admin

    def post_FAQ(self):
        self.faq_as_student = Question(True, '?', "aaaaaaa", self.student)
        self.faq_as_admin = Question(True, '???', "BbBbBb", self.admin)
        self.assertFalse(self.faq_as_student.isFAQ)
        self.assertTrue(self.faq_as_admin.isFAQ)
        self.assertEqual('?', self.faq_as_student.question)
        self.assertEqual('???', self.faq_as_admin.question)
        self.assertEqual('aaaaaaa', self.faq_as_student.answer)
        self.assertEqual('BbBbBb', self.faq_as_admin.answer)
        del self.faq_as_student
        del self.faq_as_admin

    def set_FAQ(self):
        self.faq_as_student = Question(False, '?', "answer", self.student)
        self.faq_as_admin = Question(False, '???', "ANSWER", self.admin)
        self.assertFalse(self.faq_as_student.isFAQ)
        self.assertFalse(self.faq_as_admin.isFAQ)
        self.faq_as_student.set_FAQ(True, self.faq_as_student)
        self.faq_as_admin.set_FAQ(True, self.faq_as_admin)
        self.assertFalse(self.faq_as_student.isFAQ)
        self.assertTrue(self.faq_as_admin.isFAQ)
        del self.faq_as_student
        del self.faq_as_admin

    def set_answer(self):
        self.faq_as_student = Question(False, '?', "answer", self.student)
        self.faq_as_admin = Question(False, '???', "ANSWER", self.admin)
        self.faq_as_student.set_answer("")
        self.faq_as_admin.set_answer("   .   ")
        self.assertEqual("", self.faq_as_student.answer)
        self.assertEqual("   .   ", self.faq_as_admin)

    def check_linked_list_functionality(self):
        pass

    def check_date(self):
        pass

    def empty_question(self):
        pass

if __name__ == '__main__':
    unittest.main()
