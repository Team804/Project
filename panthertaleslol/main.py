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
import webapp2
import os
import urllib
import jinja2
from google.appengine.ext import ndb 0

JINJA_ENVIRONMENT = jinja2.Environment(
            loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Question(ndb.Model):
    isFAQ = ndb.BooleanProperty(required=True)
    question = ndb.StringProperty(required=True)
    answer = ndb.StringProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True, required=True)
    user = ndb.StructuredProperty(required=True)
    key = ndb.StringProperty(required=True)
    next_question_key = ndb.StringProperty()
    prev_question_key = ndb.StringProperty()

    def __init__(self, bIsFAQ, StrQuestion, StrAnswer, UserObj):
        if UserObj.type is 'Admin':
            isFAQ = bIsFAQ
        else:
            isFAQ = False
        question = StrQuestion
        answer = StrAnswer
        user = UserObj
    #   #generate self key (app engine)

    def set_answer(self, StrAnswer):
        answer = StrAnswer

    def get_answer(self):
        return answer

    def set_followup(self, StrQuestionKey):
        next_question_key = StrQuestionKey
        # [Question with key == (next_question_key)].prev_question_key = this.key
    def set_FAQ(self, bIsFAQ, StrCurrentUserKey):
    #   if ([user corresponding to StrCurrentUserKey].type = 'Admin')
    #       isFAQ = bIsFAQ





class User(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True)
    questions = ndb.StructuredProperty(Question, repeated=True)

    def __init__(self, StrUsername, StrPassword, StrType, questions):
        username = StrUsername
        password = StrPassword
        type = StrType


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # populate data store with mock info if it doesn't exist
        users = User.query().fetch()
        if not users:
            User(username='RegisterUsers', password='pass123'
                 , type='Administrator').put()
            User(username='SampleProfessor', password='uniquePass'
                 , type='Administrator').put()
            User(username='SampleStudent', password='anotherPass'
                 , type='Student').put()

        template = JINJA_ENVIRONMENT.get_template('templates/protologin.html')
        self.response.write(template.render())

    def post(self):
        pass


class StudentHome(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/StudentHomePage.html')
        self.response.write(template.render())

class AdminHome(webapp2.RequestHandler):
    def get(self):
        template= JINJA_ENVIRONMENT.get_template('templates/AdministratorHomePage.html')
        self.response.write(template.render())

class StudentQA(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/StudentQAPage.html')
        self.response.write(template.render())

class SubmitFAQ(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/submitfaq.html')
        self.response.write(template.render())

class QuestionQueue(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/QuestionQueue.html')
        self.response.write(template.render())

class FAQ(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/FAQ.html')
        self.response.write(template.render())

class FAQADMIN(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/FAQAdminView.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/studenthome', StudentHome),
    ('/adminhome', AdminHome),
    ('/studentQA', StudentQA),
    ('/submitfaq', SubmitFAQ),
    ('/protologin', MainHandler),
    ('/questionqueue', QuestionQueue),
    ('/FAQ', FAQ),
    ('/FAQADMIN', FAQADMIN)
], debug=True)
