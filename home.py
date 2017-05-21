import os
import webapp2
import jinja2
import re

template_path=os.path.join(os.path.dirname(__file__),"template")
JINGA_ENVIRONMENT=jinja2.Environment(loader=jinja2.FileSystemLoader(template_path),autoescape=True)

class handler(webapp2.RequestHandler):
    def write(self,*a):
        self.response.out.write(*a)

    def render_string(self, template, **params):
        t=JINGA_ENVIRONMENT.get_template(template)
        return t.render(params)

    def render(self, template, **params):
        self.write(self.render_string(template, **params))

class MainPage(handler):
    def get(self):
        items=self.request.get_all("items")
        self.render("mainpage.html",items=items)