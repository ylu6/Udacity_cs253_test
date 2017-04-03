import webapp2
import jinja2
import os

from google.appengine.ext import db
from pkg_resources import require

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a):
        self.response.write(*a)
        
    def render(self, template, **kw):
        t = jinja_env.get_template(template)
        html_text = t.render(kw)
        self.write(html_text)

class Blog(db.Model):
    title = db.StringProperty()
    blog = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add = True)
    
    

class MainPage(Handler):
    def render_front(self, title="", blog="", error=""):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        #self.response.write(blogs[0].title + blogs[0].blog)
        self.render("blog_mainpage.html", blogs=blogs)
        
    def get(self):
        self.render_front()
    
    

class NewpostHandler(Handler):
    def render_newpost(self, title="", blog="", error=""):
        self.render("new_post.html", title=title, blog=blog, error=error)
        
    def get(self):
        self.render_newpost()
        
    def post(self):
        title = self.request.get('title')
        blog = self.request.get('blog')
        
        if title and blog:
            b = Blog(title = title, blog = blog)
            b.put()
            
            #self.redirect('/')
        else:
            error = "we need both a title and some blog content!"
            self.render_newpost(title, blog, error)
    
application = webapp2.WSGIApplication([('/', MainPage),
                                       ('/newpost', NewpostHandler)], debug=True)
