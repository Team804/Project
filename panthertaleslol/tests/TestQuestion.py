import unittest
from panthertaleslol.main import Question
from panthertaleslol.main import User

class TestQuestion(unittest.TestCase):
    def setup(self):
        self.student = User('student', 'password', 'Student', "")
        self.admin = User('admin', 'password', 'Admin', "")

    def tearDown(self):
        del self.defaultQuestion

    def post_FAQ(self):
        self.faq_as_student = Question(True, '?', "aaaaaaa", self.student)
        self.faq_as_admin = Question(True, '???', "BbBbBb", self.admin)
        assert False(self.faq_as_student.isFAQ)
        assert True(self.faq_as_admin.isFAQ)
        assert '?'(self.faq_as_student.question)
        assert '???'(self.faq_as_admin.question)
        assert 'aaaaaaa'(self.faq_as_student.answer)
        assert 'BbBbBb'(self.faq_as_admin.answer)
        del self.faq_as_student
        del self.faq_as_admin

    def set_FAQ(self):
        self.faq_as_student = Question(False, '?', "answer", self.student)
        self.faq_as_admin = Question(False, '???', "ANSWER", self.admin)
        pass

    def set_answer(self):
        self.question = Question()
        #as student, fails
        #as admin
        pass

    def check_linked_list_functionality(self):
        pass

    def check_date(self):
        pass

    def empty_question(self):
        pass






if __name__ == '__main__':
    unittest.main()
