
import webapp2, jinja2, os, re
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Card(db.Model):
    front = db.StringProperty(required = True)
    rear = db.StringProperty(required = True)
    display = db.BooleanProperty

class Handler(webapp2.RequestHandler):
    """ Utility class for storing methods that are used by most request handlers """

    # def initialize(self, *a, **kw):
    #     webapp2.RequestHandler.initialize(self, *a, **kw)


class MainHandler(Handler):
    """ displays the main page """
    def get(self):
        t = jinja_env.get_template("index.html")
        response = t.render()
        self.response.write(response)

class NewCardHandler(Handler):

    def render_form(self, front="", rear="", error=""):
        """ Render the new card form with or without an error, based on parameters """
        t = jinja_env.get_template("newcard.html")
        response = t.render(front=front, rear=rear, error=error)
        self.response.out.write(response)

    def get(self):
        self.render_form()

    def post(self):
        """ Create a new card if possible. Otherwise, return with an error message """
        front = self.request.get("front")
        rear = self.request.get("rear")

        if front and rear:

            # create a new Card object and store it in the database
            card = Card(
                front=front,
                rear=rear)
            card.put()

            # get the id of the new card, so we can render the post's page (via the permalink)
            id = post.key().id()
            self.redirect("/card/%s" % id)
        else:
            error = "Card must have 2 sides!"
            self.render_form(front, rear, error)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newcard', NewCardHandler)
], debug=True)
