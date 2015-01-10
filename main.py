import webapp2
import jinja2
import os

from handlers import MainHandler, AboutHandler, SearchHandler, ContactHandler, SuggestServicesHandler, ServicesHandler

def handle_404(request, response, exception):
    response.write('Page not found')
    response.set_status(404)

def handle_500(request, response, exception):
    response.write('Oops! I could swear this page was here!')
    response.set_status(500)
    
app = webapp2.WSGIApplication([
    ('/', MainHandler.MainHandler),
    ('/about', AboutHandler.AboutHandler),
    ('/search', SearchHandler.SearchHandler),
    ('/contact', ContactHandler.ContactHandler),
    ('/suggest_services', SuggestServicesHandler.SuggestServicesHandler),
    ('/mental_illness_services', ServicesHandler.ServicesHandler),
], debug=True)

app.error_handlers[404] = handle_404
#app.error_handlers[500] = handle_500
