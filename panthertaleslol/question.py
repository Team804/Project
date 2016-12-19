# Question NBD Model Class


from google.appengine.ext import ndb


class Question(ndb.Model):
    isFAQ = ndb.BooleanProperty(required=True)
    question = ndb.StringProperty(required=True)
    answer = ndb.StringProperty()  # response field written straight to question
    username = ndb.StringProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    date_answered = ndb.DateTimeProperty(auto_now=True)
    # bool flag to see if question has been looked at for future implementation maybe?
    unAnswered = ndb.BooleanProperty(default=True)
    answeredBy = ndb.StringProperty()

    def get_url_safe_key(self):
        return self.key.urlsafe()


    @staticmethod
    def get_question_from_url_safe_key(urlsafe_key):
        question_key = ndb.Key(urlsafe=urlsafe_key)
        question = question_key.get()
        return question
