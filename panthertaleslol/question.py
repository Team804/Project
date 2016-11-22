# Question NBD Model Class

from google.appengine.ext import ndb


class Question(ndb.Model):
    isFAQ = ndb.BooleanProperty(required=True)
    question = ndb.StringProperty(required=True)
    answer = ndb.StringProperty()  # response field written straight to question
    date_created = ndb.DateTimeProperty(auto_now_add=True, required=True)
    # bool flag to see if question has been looked at for future implementation maybe?
    unSeen = ndb.BooleanProperty(required=True)

    def get(self):
        questions = Question.query().fetch()

        if not questions:
            Question(isFAQ=True, question='Why does Kyle hate us?',
                     answer='He wont even invite us to Thanksgiving :(').put()
            Question(isFAQ=True, question='Seriously, Kyle doesnt even like penguins',
                     answer='What is wrong with that man?').put()

    def post(self):
        pass

    # method to set an answer
    def set_answer(self, answer):
        # TODO check active session user type if prof
        # if 'user_name' in self.session and self.session['user_name']:
        #   current_user = User.query(user_name = self.session['user_name']
        #   if current_user.type == "Administrator":
        #       self.answer = answer
        #       return True
        #   else:
        #       return False
        return False

    def set_followup(self, question):
        # disliked structured properties so will need to go with key methodology after all
        # self.next_question = question
        # self.next_question.prev_question = self
        return False

    # method to flag Question as an FAQ
    def set_as_FAQ(self, isFAQ, CurrentUser):
        # if 'user_name' in self.session and self.session['user_name']:
        #   current_user = User.query(user_name = self.session['user_name']
        #   if current_user.type == "Administrator":
        #       self.isFAQ = isFAQ
        #       return True
        #   else:
        return False