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
            Professor(user_name='SampleProfessor', password='pass123', first_name='Jason', last_name='Rock').put()
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
            users = User.query(User.user_name == entered_username).fetch()
            logging.info(users)
            if not users:
                self.redirect('/')
            else:

                logging.info(User.query(User.user_name == entered_username).fetch()[0].first_login)
                # check if it's their first time logging in, sent em to different page then
                if User.query(User.user_name == entered_username).fetch()[0].first_login:
                    self.session['username'] = entered_username
                    self.redirect('/myFirstLogin')
                else:
                    profs = Professor.query(Professor.user_name == entered_username).fetch()
                    if profs:
                        current_user = profs[0]
                        if entered_password != current_user.password:
                            self.redirect('/')
                        else:
                            self.session['username'] = entered_username
                            self.redirect('/adminhome')
                    else:
                        students = Student.query(Student.user_name == entered_username).fetch()
                        current_user = students[0]
                        if entered_password != current_user.password:
                            self.redirect('/')
                        else:
                            self.session['username'] = entered_username
                            self.redirect('/studenthome')

class StudentHome(BaseHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/StudentHomePage.html')
        self.response.write(template.render())


class AdminHome(BaseHandler):
    def get(self):
        template= JINJA_ENVIRONMENT.get_template('templates/AdministratorHomePage.html')
        self.response.write(template.render())


class SubmitQuestion(BaseHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/submitquestion.html')
        self.response.write(template.render())


class SubmitFAQ(BaseHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/submitfaq.html')
        self.response.write(template.render())
    def post(self):
        template = JINJA_ENVIRONMENT.get_template('templates/submitfaq.html')

        self.response.write(template.render( {

        }))
        Question(isFAQ=True, question=self.request.get('question'), answer=self.request.get('answer')).put()
        self.redirect('FAQAdminView')


class QuestionQueue(BaseHandler):
    def get(self):
        if 'username' in self.session and self.session['username']:
            username = self.session['username']
            user = Professor.query(Professor.user_name == username).fetch()
            qqtab=1
            if self.request.get('NewQ'):
                qqtab=1
            elif self.request.get('RecentQ'):
                qqtab=2
            elif self.request.get('ByStudent'):
                qqtab=3
            if user:
                user = user[0]
                q1 = Question(isFAQ=True, question='Why does Kyle hate us?',
                              answer='He wont even invite us to Thanksgiving :(')
                q2 = Question(isFAQ=True, question='Seriously, Kyle doesnt even like penguins',
                              answer='What is wrong with that man?')
                q3 = Question(isFAQ=False, question='Seriously, Kyle doesnt even like penguins',
                              answer='What is wrong with that man?')
                template = JINJA_ENVIRONMENT.get_template('templates/QuestionQueue.html')
                self.response.write(template.render({
                    'user': user,
                    'q1s': q1.question,
                    'q2s': q2.question,
                    'q3s': q3.question,
                    'QQTAB': qqtab
                }))
        else:
            self.redirect('/')


class FAQ(BaseHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/FAQ.html')

        questions = Question.query().fetch()
        q1 = Question(isFAQ=True, question='Why does Kyle hate us?',
                     answer='He wont even invite us to Thanksgiving :(')
        q2 = Question(isFAQ=True, question='Seriously, Kyle doesnt even like penguins',
                     answer='What is wrong with that man?')
        q3 = Question(isFAQ=False, question='Seriously, Kyle doesnt even like penguins',
                      answer='What is wrong with that man?')
        tempQuestions = []
        tempQuestions.append(q1)
        tempQuestions.append(q2)
        tempQuestions.append(q3)

        self.response.write(template.render( {
            'questions':tempQuestions
            } ))

        if not questions:
            questions = []
            Question(isFAQ=True, question='Why does Kyle hate us?',
                     answer='He wont even invite us to Thanksgiving :(').put()
            Question(isFAQ=True, question='Seriously, Kyle doesnt even like penguins',
                     answer='What is wrong with that man?').put()


class FAQADMIN(BaseHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/FAQAdminView.html')

        questions = Question.query().fetch()
        q1 = Question(isFAQ=True, question='Why does Kyle hate us?',
                     answer='He wont even invite us to Thanksgiving :(')
        q2 = Question(isFAQ=True, question='Seriously, Kyle doesnt even like penguins',
                     answer='What is wrong with that man?')
        q3 = Question(isFAQ=False, question='Seriously, Kyle doesnt even like penguins',
                      answer='What is wrong with that man?')
        tempQuestions = []
        tempQuestions.append(q1)
        tempQuestions.append(q2)
        tempQuestions.append(q3)

        self.response.write(template.render( {
            'str':q1.question,
            'questions':tempQuestions
            } ))

        Question(isFAQ=True, question='Why does Kyle hate us?',
                 answer='He wont even invite us to Thanksgiving :(').put()
        Question(isFAQ=True, question='Seriously, Kyle doesnt even like penguins',
                 answer='What is wrong with that man?').put()
        questions = Question.query().fetch()

    def post(self):
        template = JINJA_ENVIRONMENT.get_template('templates/FAQAdminView.html')

        self.response.write(template.render( {

            } ))

class FAQDelete(BaseHandler):
    def post(self):
        template = JINJA_ENVIRONMENT.get_template('templates/FAQAdminView.html')

        self.response.write(template.render( {

            } ))

class LogoutHandler(BaseHandler):
    def get(self):
        if 'username' in self.session:
            self.session.pop('username')
        self.redirect('/')

config = {
    'webapp2_extras.sessions': {
            'secret_key': 'my-secret-key'
        }
}

class TestPage(webapp2.RequestHandler):
    def get(self):
        testing_class = TestTests()
        testing_class.list_results_all[:] = []
        testing_class.run_all_tests()
        logging.info(testing_class.test_results.testsRun)
        template = JINJA_ENVIRONMENT.get_template('templates/testPage.html')
        logging.info(len(testing_class.list_results_all))
        self.response.write(template.render({'test_results':testing_class.list_results_all}))

class RegisterStudents(BaseHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/RegisterStudentsPage.html')
        self.response.write(template.render())
    def post(self):
        input_list = self.request.get('inputText')
        logging.info(input_list)
        self.parse_info(input_list)
        self.redirect('/')

    def parse_info(self, input_list):

        input_list = input_list.replace(' ','')

        while len(input_list) > 5:

            pos = input_list.find(',')
            l_name = input_list[0:pos].replace(',','')
            input_list = input_list[pos:len(input_list)]
            logging.info(l_name)

            pos = input_list.find(',')
            f_name = input_list[0:pos].replace(',','')
            input_list = input_list[pos:len(input_list)]
            logging.info(f_name)

            pos = input_list.find(',')
            u_name = input_list[0:pos].replace(',','')
            input_list = input_list[pos:len(input_list)]
            logging.info(u_name)

            pos = input_list.find('\n')
            type = input_list[0:pos].replace(',','')
            input_list = input_list[pos:len(input_list)]
            logging.info(type)

            # add user
            if type == "Instructor":
                Professor(first_name=f_name, last_name=l_name, user_name=u_name, password="123").put()
            else:
                Student(first_name=f_name, last_name=l_name, user_name=u_name, password="234").put()

class FirstLogin(BaseHandler):
    def get(self):
        username = self.session['username']
        logging.info(username)
        user = User.query(User.user_name == username).fetch()
        user = user[0]
        logging.info(user)

        template = JINJA_ENVIRONMENT.get_template('templates/firstlogin.html')
        self.response.write(template.render({'user':user, 'first_time':True}))
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
                self.response.write(template.render({'user': user, 'first_time':False}))
        else:
            template = JINJA_ENVIRONMENT.get_template('templates/firstlogin.html')
            self.response.write(template.render({'user': user, 'first_time':False, 'password_match': False}))


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
    ('/protologin', MainHandler),
    ('/questionqueue', QuestionQueue),
    ('/FAQ', FAQ),
    ('/FAQADMIN', FAQADMIN),
    ('/FAQDelete', FAQDelete),
    ('/registerStudents', RegisterStudents),
    ('/logout', LogoutHandler),
    ('/testpage', TestPage),
    ('/myFirstLogin', FirstLogin),
    ('/', MainHandler)
], debug=True, config=config)
