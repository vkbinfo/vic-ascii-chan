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

class Blog(db.Model):
    subject=db.StringProperty(required=True)
    content=db.TextProperty(required=True)
    created_on=db.DateTimeProperty(auto_now_add=True)

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
        arts=db.GqlQuery("SELECT * FROM Art order by time DESC")
        self.render("front.html",art=art,title=title,error=error,arts=arts)

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
            newData=Art(title=title,art=art)
            newData.put()
            self.write("wow, cool--> YOu go vic with patience")


class NewPost(handler):
    def render_arguments(self,title='',content='',error=''):
        self.render("newpost.html",title=title,
                    content=content,error=error)

    def get(self):
        self.render("newpost.html")

    def post(self):
        title=self.request.get("subject")
        content=self.request.get("content")

        if not title and content:
            self.render_arguments(content=content,
                                  error="Please also submit subject name.")
        elif title and not content:
            self.render_arguments(title=title,
                                  error="Please also submit content.")
        elif not title and not content:
            self.render_arguments(error="please submit both subject"
                                        "and Content")
        else:
            new_post=Blog(subject=title,content= content)
            new_post.put()
            self.redirect("/blog/"+str(new_post.key().id()))

class BlogPage(handler):
    def get(self):
        blogs=db.GqlQuery("select * from Blog order by created_on DESC")
        self.render("blog.html",blogs=blogs)

class paramlink(handler):
    def get(self,key_id):
        #Getting data by key ID
        data=Blog.get_by_id(int(key_id))
        self.render("paramlink.html", data=data)

app = webapp2.WSGIApplication([
    ('/', MainPage), ("/blog",BlogPage),
    ('/blog/newpost', NewPost), ("/blog/([0-9]+)",paramlink)
], debug=True)
