#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from user import Student
from user import Professor
from user import User
from question import Question
from testTests import TestTests
import logging
import webapp2
import os
import jinja2
import time
from testTests import TestTests
from webapp2_extras import sessions



JINJA_ENVIRONMENT = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)

        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            return self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()


class MainHandler(BaseHandler):
    def get(self):
        # populate data store with mock info if it doesn't exist
        users = User.query().fetch()
        if not users:
            Professor(user_name='SampleProfessor', password='pass123', first_name='Jayson', last_name='Rock').put()
            Student(user_name='SampleStudent', password='pass234', first_name='Kylie', last_name='Weber').put()

        if 'username' in self.session and self.session['username']:
            username = self.session['username']
            profs = Professor.query(Professor.user_name == username).fetch()
            if profs:
                self.redirect('/adminhome')
            else:
                self.redirect('/studenthome')
        else:
            template = JINJA_ENVIRONMENT.get_template('templates/protologin.html')
            self.response.write(template.render())

    def post(self):
        if 'username' in self.session and self.session['username']:
            username = self.session['username']
            profs = Professor.query(Professor.user_name == username).fetch()
            if profs:
                self.redirect('/adminhome')
            else:
                self.redirect('/studenthome')
        else:
            entered_username = self.request.get('username')
            entered_password = self.request.get('password')
            user = User.query(User.user_name == entered_username).fetch()[0]
            if user and entered_password == user.password:
                # check if it's their first time logging in, sent em to different page then
                if user.first_login:
                    self.session['username'] = entered_username
                    self.redirect('/myFirstLogin')
                else:
                    # profs = Professor.query(Professor.user_name == entered_username).fetch()
                    if user is Professor:
                        self.session['username'] = entered_username
                        self.redirect('/adminhome')
                    else:
                        if entered_password != user.password:
                            self.redirect('/')
                        else:
                            self.session['username'] = entered_username
                            self.redirect('/studenthome')
            else:
                self.redirect('/')


class StudentHome(BaseHandler):
    def get(self):
        if 'username' in self.session and self.session['username']:
            username = self.session['username']
            students = Student.query(Student.user_name == username).fetch()
            if students:
                student = students[0]
                template = JINJA_ENVIRONMENT.get_template('templates/StudentHomePage.html')
                self.response.write(template.render({
                    'answered_questions': student.get_answered_questions,
                    'unanswered_questions': student.get_unanswered_questions,
                    'user': student.first_name+" "+student.last_name
                }))
            else:
                self.response.write("Invalid Credentials")
                self.redirect('/')
        else:
            self.response.write("Invalid Credentials")
            self.redirect('/')


class AdminHome(BaseHandler):
    def get(self):
        questions = list(Question.query().fetch())
        render_parameter = {'questions': questions}
        if 'username' in self.session and self.session['username']:
            username = self.session['username']
            profs = Professor.query(Professor.user_name == username).fetch()
            prof = profs[0]
            if profs:
                render_parameter['username'] = prof.first_name + " " + prof.last_name
                template = JINJA_ENVIRONMENT.get_template('templates/AdministratorHomePage.html')
                self.response.write(template.render(render_parameter))
            else:
                html = """<html>
                <head><meta http-equiv="refresh" content="3;URL='/'"><title>Redirect</title></head>
                <body style="color: red;"> Invalid Credentials, you are being redirected.</body></html>
                """
                self.response.write(html)
        else:
            html="""<html>
            <head><meta http-equiv="refresh" content="3;URL='/'"><title>Redirect</title></head>
            <body style="color: red;"> Invalid Credentials, you are being redirected.</body></html>
            """
            self.response.write(html)

    def post(self):
        question = self.request.get('q')
        question.answer = self.request.get('txtInput')

        template = JINJA_ENVIRONMENT.get_template('templates/AdministratorHomePage.html')
        self.response.write(template.render())


class StudentAccountSettings(BaseHandler):
    def get(self):
        username = self.session['username']
        logging.info(username)
        students = Student.query(Student.user_name == username).fetch()
        student = students[0]
        if student:
            logging.info(student)
            template = JINJA_ENVIRONMENT.get_template('templates/StudentAccountSettingsPage.html')
            self.response.write(template.render({'user': student}))
        else:
            html="""<html>
            <head><meta http-equiv="refresh" content="3;URL='/'"><title>Redirect</title></head>
            <body style="color: red;"> Invalid Credentials, you are being redirected.</body></html>
            """
            self.response.write(html)

    def post(self):
        username = self.session['username']
        logging.info(username)
        student = Student.query(Student.user_name == username).fetch()[0]
        if self.request.get('first_pass') == self.request.get('second_pass'): #check if passwords match
            logging.info(self.request.get('first_pass'))
            if student.change_password(self.request.get('first_pass')): # password change successful
                student.put()
                self.redirect('/')
            else:
                template = JINJA_ENVIRONMENT.get_template('templates/StudentAccountSettingsPage.html')
                self.response.write(template.render({'user': student}))
        else:
            template = JINJA_ENVIRONMENT.get_template('templates/StudentAccountSettingsPage.html')
            self.response.write(template.render({'user': student, 'password_match': False}))


class AdminAccountSettings(BaseHandler):
    def get(self):
        username = self.session['username']
        logging.info(username)
        profs = Professor.query(Professor.user_name == username).fetch()
        prof = profs[0]
        if prof:
            logging.info(prof)
            template = JINJA_ENVIRONMENT.get_template('templates/AdminAccountSettingsPage.html')
            self.response.write(template.render({'user': prof}))
        else:
            html="""<html>
            <head><meta http-equiv="refresh" content="3;URL='/'"><title>Redirect</title></head>
            <body style="color: red;"> Invalid Credentials, you are being redirected.</body></html>
            """
            self.response.write(html)

    def post(self):
        username = self.session['username']
        logging.info(username)
        prof = Professor.query(Professor.user_name == username).fetch()[0]
        if not prof:
            html="""<html>
            <head><meta http-equiv="refresh" content="3;URL='/'"><title>Redirect</title></head>
            <body style="color: red;"> Invalid Credentials, you are being redirected.</body></html>
            """
            self.response.write(html)
        else:
            if self.request.get('first_pass') == self.request.get('second_pass'): #check if passwords match
                logging.info(self.request.get('first_pass'))
                if prof.change_password(self.request.get('first_pass')): # password change successful
                    prof.put()
                    self.redirect('/')
                else:
                    template = JINJA_ENVIRONMENT.get_template('templates/AdminAccountSettingsPage.html')
                    self.response.write(template.render({'user': prof}))
            else:
                template = JINJA_ENVIRONMENT.get_template('templates/AdminAccountSettingsPage.html')
                self.response.write(template.render({'user': prof, 'password_match': False}))


class SubmitQuestion(BaseHandler):
    def get(self):
        if 'username' in self.session and self.session['username']:
            username = self.session['username']
            students = Student.query(Student.user_name == username).fetch()
            if students:
                template = JINJA_ENVIRONMENT.get_template('templates/submitquestion.html')
                self.response.write(template.render({
                    'submitagain': False,
                    'emptyfield': False
                }))
            else:
                html = """<html>
                <head><meta http-equiv="refresh" content="3;URL='/'"><title>Redirect</title></head>
                <body style="color: red;"> Invalid Credentials, you are being redirected.</body></html>
                """
                self.response.write(html)
        else:
            html="""<html>
            <head><meta http-equiv="refresh" content="3;URL='/'"><title>Redirect</title></head>
            <body style="color: red;"> Invalid Credentials, you are being redirected.</body></html>
            """
            self.response.write(html)

    def post(self):
        question = self.request.get('questionInput')
        if len(question) > 0:
            logging.info(question)
            username = self.session['username']
            user = User.query(User.user_name == username).fetch()
            user_key = user[0].key
            Question(parent=user_key, question=question, username=username, isFAQ=False).put()
            template = JINJA_ENVIRONMENT.get_template('templates/submitquestion.html')
            self.response.write(template.render({
                'submitagain': True}))
        else:
            template = JINJA_ENVIRONMENT.get_template('templates/submitquestion.html')
            self.response.write(template.render({
                'emptyfield': True,
                'nosubmit': True
            }))


class SubmitFAQ(BaseHandler):  # what is this even for?
    def get(self):
        if 'username' in self.session and self.session['username']:
            html = """<form action='/submitfaq' method = 'POST'>
            <textarea name = "inputtedQ" rows = "15" cols = "50" style="placeholder="Question goes here...">
            </textarea>
            <textarea name = "inputtedA" rows = "15" cols = "50" placeholder="Answer goes here...">
            </textarea>
            <input type="submit" value="submit">
            </form>
            """
            # self.response.write(html)
            template = JINJA_ENVIRONMENT.get_template('templates/submitfaq.html')
            self.response.write(template.render())
        else:
            html="""<html>
            <head><meta http-equiv="refresh" content="3;URL='/'"><title>Redirect</title></head>
            <body style="color: red;"> Invalid Credentials, you are being redirected.</body></html>
            """
            self.response.write(html)

    def post(self):
        # Question(isFAQ=True, question=self.request.get('inputtedQ'), answer=self.request.get('inputtedA')).put()
        Question(isFAQ=True, question=self.request.get('question'), answer=self.request.get('answer')).put()
        self.redirect('/FAQADMIN')


class QuestionQueue(BaseHandler):
    def get(self):
        unanswered_questions = Question.query(Question.unAnswered == True).order(-Question.date_created).fetch()
        recent_questions = Question.query().order(-Question.date_answered).fetch(6)
        students = Student.query().fetch()
        if 'username' in self.session and self.session['username']:
            username = self.session['username']
            profs = Professor.query(Professor.user_name == username).fetch()
            qqtab = 1
            if self.request.get('NewQ'):
                qqtab = 1
            elif self.request.get('RecentQ'):
                qqtab = 2
            elif self.request.get('ByStudent'):
                qqtab = 3
            elif self.request.get('FAQs'):
                self.redirect('/FAQADMIN')
            if profs:
                template = JINJA_ENVIRONMENT.get_template('templates/QuestionQueue.html')
                self.response.write(template.render({
                    'QQTAB': qqtab,
                    'unanswered_questions': unanswered_questions,
                    'recent_questions': recent_questions,
                    'students': students
                }))
            else:
                html = """<html>
                <head><meta http-equiv="refresh" content="3;URL='/'"><title>Redirect</title></head>
                <body style="color: red;"> Invalid Credentials, you are being redirected.</body></html>
                """
                self.response.write(html)
        else:
            html="""<html>
            <head><meta http-equiv="refresh" content="3;URL='/'"><title>Redirect</title></head>
            <body style="color: red;"> Invalid Credentials, you are being redirected.</body></html>
            """
            self.response.write(html)

    def post(self):
        if self.request.get('Answer'):
            qurl=self.request.get('Answer')
            qkey = Question().get_question_from_url_safe_key(qurl)
            qkey.answer=self.request.get('answerin')
            qkey.unAnswered = False
            qkey.put()
        elif self.request.get('MakeFAQ'):
            qurl=self.request.get('MakeFAQ')
            qkey = Question().get_question_from_url_safe_key(qurl)
            qkey.isFAQ = True
            qkey.put()
        else:
            qurl=self.request.get('Delete')
            qkey = Question().get_question_from_url_safe_key(qurl)
            qkey.key.delete()

        self.redirect('/questionqueue')


class FAQPublic(BaseHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/FAQPublic.html')
        questions = Question.query(Question.isFAQ == True).order(-Question.date_created).fetch()
        self.response.write(template.render({
            'questions': questions
        }))

		
class FAQ(BaseHandler):
    def get(self):
        if 'username' in self.session and self.session['username']:
            template = JINJA_ENVIRONMENT.get_template('templates/FAQ.html')
            questions = Question.query(Question.isFAQ == True).order(-Question.date_created).fetch()
            self.response.write(template.render({
                'questions': questions
            }))
        else:
            self.redirect('/')


class FAQADMIN(BaseHandler):
    def get(self):
        if 'username' in self.session and self.session['username']:
            template = JINJA_ENVIRONMENT.get_template('templates/FAQAdminView.html')
            questions = Question.query(Question.isFAQ == True).order(-Question.date_created).fetch()
            logging.info(questions)
            self.response.write(template.render({
                'questions': questions
            }))
        else:
            html = """<html>
            <head><meta http-equiv="refresh" content="3;URL='/'"><title>Redirect</title></head>
            <body style="color: red;"> Invalid Credentials, you are being redirected.</body></html>
            """
            self.response.write(html)

    def post(self):
        template = JINJA_ENVIRONMENT.get_template('templates/FAQAdminView.html')
        self.request.get("q")
        self.response.write(template.render({}))


class FAQDelete(BaseHandler):
    def get(self):
        #get the url path
        url_key = self.request.path
        question_key = url_key.replace("/FAQADMIN/D/", "")
        question_key = Question().get_question_from_url_safe_key(question_key)
        logging.info(question_key)
        question_key.key.delete()
        self.redirect('/FAQADMIN')

class FAQEdit(BaseHandler):
    def get(self):
        url_key = self.request.path
        question_key = url_key.replace("/FAQADMIN/E/", "")
        question = Question().get_question_from_url_safe_key(question_key)

        template = JINJA_ENVIRONMENT.get_template('templates/FAQAdminView.html')
        questions = Question.query().fetch()
        self.response.write(template.render({
            'questions': questions,
            'questionBeingEdited': question
        }))
        # self.redirect('/FAQADMIN')
    def post(self):
        url_key = self.request.path
        question_key = url_key.replace("/FAQADMIN/E/", "")
        question = Question().get_question_from_url_safe_key(question_key)
        question.answer = self.response.get('editFAQ')
        question.put()

        template = JINJA_ENVIRONMENT.get_template('templates/FAQAdminView.html')
        questions = Question.query().fetch()
        self.response.write(template.render({
            'questions': questions,
            'questionBeingEdited': question
        }))
        # self.redirect('/FAQADMIN')

class LogoutHandler(BaseHandler):
    def get(self):
        if 'username' in self.session:
            self.session.pop('username')
        self.redirect('/')


class TestPage(webapp2.RequestHandler):
    def get(self):
        testing_class = TestTests()
        testing_class.list_results_all[:] = []
        testing_class.run_all_tests()
        logging.info(testing_class.test_results.testsRun)
        template = JINJA_ENVIRONMENT.get_template('templates/testPage.html')
        logging.info(len(testing_class.list_results_all))
        self.response.write(template.render({'test_results': testing_class.list_results_all}))


class RegisterStudents(BaseHandler):
    def get(self):
        if 'username' in self.session and self.session['username']:
            username = self.session['username']
            profs = Professor.query(Professor.user_name == username).fetch()
            if profs:
                template = JINJA_ENVIRONMENT.get_template('templates/RegisterStudentsPage.html')
                self.response.write(template.render())
            else:
                html = """<html>
                <head><meta http-equiv="refresh" content="3;URL='/'"><title>Redirect</title></head>
                <body style="color: red;"> Invalid Credentials, you are being redirected.</body></html>
                """
                self.response.write(html)
        else:
            html="""<html>
            <head><meta http-equiv="refresh" content="3;URL='/'"><title>Redirect</title></head>
            <body style="color: red;"> Invalid Credentials, you are being redirected.</body></html>
            """
            self.response.write(html)


    def post(self):
        input_list = self.request.get('inputText')
        logging.info(input_list)
        parse_info(input_list)

        logging.info("Registered users")
        self.redirect('/')


def parse_info(input_list):
    input_list = input_list.replace(' ','')
    logging.info("parse info called")
    while len(input_list) > 5:

        pos = input_list.find(',')
        l_name = input_list[0:pos]
        input_list = input_list[pos+1:len(input_list)]
        logging.info("name" + l_name)

        pos = input_list.find(',')
        f_name = input_list[0:pos]
        input_list = input_list[pos+1:len(input_list)]
        logging.info(f_name)

        pos = input_list.find(',')
        u_name = input_list[0:pos]
        input_list = input_list[pos+1:len(input_list)]
        logging.info(u_name)

        pos = input_list.find('\n')
        if pos < 0:
            pos = len(input_list)
        u_type = input_list[0:pos]
        input_list = input_list[pos+1:len(input_list)]
        logging.info(u_type)

        # add user
        if u_type == "Instructor":
            prof = Professor(first_name=f_name, last_name=l_name, user_name=u_name, password="professor").put()
            logging.info(prof)
        else:
            stud = Student(first_name=f_name, last_name=l_name, user_name=u_name, password="student").put()
            logging.info(stud)


class FirstLogin(BaseHandler):
    def get(self):
        username = self.session['username']
        logging.info(username)
        user = User.query(User.user_name == username).fetch()
        user = user[0]
        logging.info(user)

        template = JINJA_ENVIRONMENT.get_template('templates/firstlogin.html')
        self.response.write(template.render({'user': user, 'first_time': True}))

    def post(self):
        username = self.session['username']
        logging.info(username)
        user = User.query(User.user_name == username).fetch()[0]
        if self.request.get('first_pass') == self.request.get('second_pass'): #check if passwords match
            logging.info(self.request.get('first_pass'))
            if user.change_password(self.request.get('first_pass')): # password change successful
                user.first_login = False
                logging.info(user.first_login)
                user.put()
                self.redirect('/')
            else:
                template = JINJA_ENVIRONMENT.get_template('templates/firstlogin.html')
                self.response.write(template.render({'user': user, 'first_time': False}))
        else:
            template = JINJA_ENVIRONMENT.get_template('templates/firstlogin.html')
            self.response.write(template.render({'user': user, 'first_time': False, 'password_match': False}))



config = {
    'webapp2_extras.sessions': {
            'secret_key': 'my-secret-key'
        }
}

app = webapp2.WSGIApplication([
    ('/studenthome', StudentHome),
    ('/adminhome', AdminHome),
    ('/submitquestion', SubmitQuestion),
    ('/submitfaq', SubmitFAQ),
    ('/studentaccountsettings', StudentAccountSettings),
    ('/adminaccountsettings', AdminAccountSettings),
    ('/protologin', MainHandler),
    ('/questionqueue', QuestionQueue),
	('/FAQPublic', FAQ),
    ('/FAQ', FAQ),
    ('/FAQADMIN', FAQADMIN),
    ('/FAQADMIN/D/.*', FAQDelete),
    ('/FAQADMIN/E/.*', FAQEdit),
    ('/registerStudents', RegisterStudents),
    ('/logout', LogoutHandler),
    ('/testpage', TestPage),
    ('/myFirstLogin', FirstLogin),
    ('/', MainHandler)
], debug=True, config=config)
