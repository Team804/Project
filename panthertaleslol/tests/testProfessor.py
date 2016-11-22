import unittest
from panthertaleslol.question import Question
from panthertaleslol.user import Professor

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


suite = unittest.TestLoader().loadTestsFromTestCase(TestProfessor)
unittest.TextTestRunner(verbosity=2).run(suite)
