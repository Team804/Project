# User NBD Model Class
import re
from question import Question
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class User(polymodel.PolyModel):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    user_name = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)

    def change_password(self, newPassword):
        if newPassword: #non empty password
            if len(newPassword) > 3: # password length
                number = re.search(r'\d+', newPassword).group()
                if len(number) > 0: # have number in pass
                    self.password = newPassword
                    return True
        return False

    # method to check uniqueness of setting user names
    def set_user_name(self, userName):
        username_list = User.query(user_name=userName).fetch()
        if username_list: #username alredy in use
            return False
        else:
            self.user_name = userName
            return True

class Student(User):
    # get all the student's submitted questions
    @property
    def get_all_questions(self):
        return Question.query(ancestor=self.key).fetch()

    # method to get unseen questions
    @property
    def get_all_unseen_questions(self, items):
        return Question.query(Question.unSeen(True), ancestor=self.key).fetch()


class Professor(User):
    @property
    def load_queue(self):
        return Question.query().fetch()
