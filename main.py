import webapp2
import jinja2
import os

from handlers.static_pages import AboutHandler, ContactHandler, MainHandler, SearchHandler, ServicesHandler, SuggestServicesHandler, ManualHandler
from handlers.admin import IndexHandler, UsersIndexHandler, NewUserHandler, EmailEndpointHandler, DashboardHandler, DashboardItemHandler, UserDashboardHandler, UserDashboardItemHandler
from handlers.users import EditHandler, LoginHandler, LogoutHandler, ProfileHandler, ResetPasswordHandler, SetPasswordHandler, DeleteHandler
from handlers.api.users import ApiLoginHandler
from handlers.admin.organizations import AdminOrgIndexHandler, AdminOrgNewHandler, AdminOrgEditHandler, AdminOrgDeleteHandler
from handlers.admin.programs import AdminProgramIndexHandler, AdminProgramNewHandler, AdminProgramEditHandler, AdminProgramDeleteHandler
from handlers.admin.services import AdminServiceIndexHandler, AdminServiceNewHandler, AdminServiceEditHandler, AdminServiceDeleteHandler
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'LK@#J$LK@#J$@#IUR(E*R)WE(FIUAFOJOWE%IUQ#)(%*TU$OIJQTJRWKGUWRE(T*W)$#(*%W$#%OIJRWOIEUWR"0t9*',
}

#from models import User

#user = User.User(name = "admin", email = "admin@example.com", organization = "org", phone = "phone", role = "admin", password_digest = User.hash_password("secret"), email_authorized = True)
#user.put()

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
    ('/manual', ManualHandler.ManualHandler),
    ('/admin', IndexHandler.IndexHandler),
    ('/admin/users', UsersIndexHandler.UsersIndexHandler),
    ('/admin/users/new', NewUserHandler.NewUserHandler),
    ('/admin/users/dashboard', UserDashboardHandler.UserDashboardHandler),
    ('/admin/users_dashboard/([^/]+)', UserDashboardItemHandler.UserDashboardItemHandler),
    ('/admin/users/([^/]+)', EmailEndpointHandler.EmailEndpointHandler),
    ('/admin/dashboard', DashboardHandler.DashboardHandler),
    ('/admin/dashboard/([^/]+)', DashboardItemHandler.DashboardItemHandler),
    ('/admin/organizations', AdminOrgIndexHandler.AdminOrgIndexHandler),
    ('/admin/organizations/new', AdminOrgNewHandler.AdminOrgNewHandler),
    ('/organizations/([^/]+)/edit', AdminOrgEditHandler.AdminOrgEditHandler),
    ('/organizations/([^/]+)/delete', AdminOrgDeleteHandler.AdminOrgDeleteHandler),
    ('/admin/programs', AdminProgramIndexHandler.AdminProgramIndexHandler),
    ('/admin/programs/new', AdminProgramNewHandler.AdminProgramNewHandler),
    ('/programs/([^/]+)/edit', AdminProgramEditHandler.AdminProgramEditHandler),
    ('/programs/([^/]+)/delete', AdminProgramDeleteHandler.AdminProgramDeleteHandler),
    ('/admin/services', AdminServiceIndexHandler.AdminServiceIndexHandler),
    ('/admin/services/new', AdminServiceNewHandler.AdminServiceNewHandler),
    ('/services/([^/]+)/edit', AdminServiceEditHandler.AdminServiceEditHandler),
    ('/services/([^/]+)/delete', AdminServiceDeleteHandler.AdminServiceDeleteHandler),
    ('/users/([^/]+)/edit', EditHandler.EditHandler),
    ('/users/([^/]+)/delete', DeleteHandler.DeleteHandler),
    ('/users/login', LoginHandler.LoginHandler),
    ('/users/logout', LogoutHandler.LogoutHandler),
    ('/users/profile', ProfileHandler.ProfileHandler),
    ('/users/reset_password', ResetPasswordHandler.ResetPasswordHandler),
    ('/users/set_password/([^/]+)', SetPasswordHandler.SetPasswordHandler),
    #('/api/users/login', ApiLoginHandler.ApiLoginHandler),

], config=config, debug=True)

app.error_handlers[404] = handle_404
#app.error_handlers[500] = handle_500
