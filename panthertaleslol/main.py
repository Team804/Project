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
import logging
import webapp2
import os
import jinja2
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
            Professor(user_name='SampleProfessor', password='pass123').put()
            Student(user_name='SampleStudent', password='pass234').put()
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


class StudentQA(BaseHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/StudentQAPage.html')
        self.response.write(template.render())


class SubmitFAQ(BaseHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/submitfaq.html')
        self.response.write(template.render())


class QuestionQueue(BaseHandler):
    def get(self):
        if 'username' in self.session and self.session['username']:
            username = self.session['username']
            user = Professor.query(Professor.user_name == username).fetch()
            qradio = self.request.get('Qradio')
            if not qradio:
                qradio = 1
            if user:
                user = user[0]
                template = JINJA_ENVIRONMENT.get_template('templates/QuestionQueue.html')
                self.response.write(template.render({
                    'user': user,
                    'QQTAB': qradio
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
            'str':q1.question,
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
            'questions':questions
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

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/studenthome', StudentHome),
    ('/adminhome', AdminHome),
    ('/studentQA', StudentQA),
    ('/submitfaq', SubmitFAQ),
    ('/protologin', MainHandler),
    ('/questionqueue', QuestionQueue),
    ('/FAQ', FAQ),
    ('/FAQADMIN', FAQADMIN),
    ('/FAQDelete', FAQDelete),
    ('/logout', LogoutHandler)
], debug=True, config=config)
