# Question NBD Model Class


from google.appengine.ext import ndb


class Question(ndb.Model):
    isFAQ = ndb.BooleanProperty(required=True)
    question = ndb.StringProperty(required=True)
    answer = ndb.StringProperty()  # response field written straight to question
    username = ndb.StringProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    # bool flag to see if question has been looked at for future implementation maybe?
    unSeen = ndb.BooleanProperty()

    def get_url_safe_key(self):
        return self.key.urlsafe()


    @staticmethod
    def get_email_from_url_safe_key(urlsafe_key):
        email_key = ndb.Key(urlsafe=urlsafe_key)
        email = email_key.get()
        return email