# Question NBD Model Class


from google.appengine.ext import ndb


class Question(ndb.Model):
    isFAQ = ndb.BooleanProperty(required=True)
    question = ndb.StringProperty(required=True)
    answer = ndb.StringProperty()  # response field written straight to question
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    # bool flag to see if question has been looked at for future implementation maybe?
    unSeen = ndb.BooleanProperty()

