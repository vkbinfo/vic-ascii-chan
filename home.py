import os
import webapp2
import jinja2
import re
from google.appengine.ext import db

template_path=os.path.join(os.path.dirname(__file__),"template")
JINGA_ENVIRONMENT=jinja2.Environment(loader=jinja2.FileSystemLoader(template_path),autoescape=True)

class Art(db.Model):
    title=db.StringProperty(required=True)
    art=db.TextProperty(required=True)
    time=db.DateTimeProperty(auto_now_add=True)

class handler(webapp2.RequestHandler):
    def write(self,*a):
        self.response.out.write(*a)

    def render_string(self, template, **params):
        t=JINGA_ENVIRONMENT.get_template(template)
        return t.render(params)

    def render(self, template, **params):
        self.write(self.render_string(template, **params))

class MainPage(handler):
    def render_page(self,art='',title='',error=''):
        self.render("front.html",art=art,title=title,error=error)

    def get(self):
        self.render_page()

    def post(self):
        title=self.request.get("title")
        art = self.request.get("art")

        if title and not art:
            self.render_page(title=title,error="You Should also input the art also.")

        elif not title and art:
            self.render_page(art=art,error="you must input title also.")

        elif not title and not art:
            self.render_page(error="you must input art and title")

        else:
            self.write("Thanks")


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
