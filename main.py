import webapp2
import jinja2
import os

from handlers.static_pages import AboutHandler, ContactHandler, MainHandler, SearchHandler, ServicesHandler, SuggestServicesHandler, ManualHandler, RecordHandler, LanguageHandler
from handlers.admin import IndexHandler, UsersIndexHandler, NewUserHandler, EmailEndpointHandler, DashboardHandler, DashboardItemHandler, UserDashboardHandler, UserDashboardItemHandler, AdminIFormBuilderHandler, AdminRecordHandler, AdminViewRecordHandler, EditRecordHandler
from handlers.users import EditHandler, LoginHandler, LogoutHandler, ProfileHandler, ResetPasswordHandler, SetPasswordHandler, DeleteHandler
from handlers.api.users import ApiLoginHandler
from handlers.admin.organizations import AdminOrgIndexHandler, AdminOrgNewHandler, AdminOrgEditHandler, AdminOrgDeleteHandler, AdminOrgDashboardHandler
from handlers.admin.programs import AdminProgramIndexHandler, AdminProgramNewHandler, AdminProgramEditHandler, AdminProgramDeleteHandler, AdminProgramDashboardHandler
from handlers.admin.services import AdminServiceIndexHandler, AdminServiceNewHandler, AdminServiceEditHandler, AdminServiceDeleteHandler, AdminServiceDashboardHandler

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'LK@#J$LK@#J$@#IUR(E*R)WE(FIUAFOJOWE%IUQ#)(%*TU$OIJQTJRWKGUWRE(T*W)$#(*%W$#%OIJRWOIEUWR"0t9*',
}

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
    #('/admin/iformbuilder_task', AdminIFormBuilderHandler.AdminIFormBuilderHandler),
    ('/admin/users', UsersIndexHandler.UsersIndexHandler),
    ('/admin/users/new', NewUserHandler.NewUserHandler),
    ('/admin/users/dashboard', UserDashboardHandler.UserDashboardHandler),
    ('/admin/users_dashboard/([^/]+)', UserDashboardItemHandler.UserDashboardItemHandler),
    ('/admin/users/([^/]+)', EmailEndpointHandler.EmailEndpointHandler),
    ('/admin/dashboard', DashboardHandler.DashboardHandler),
    ('/admin/dashboard/([^/]+)', DashboardItemHandler.DashboardItemHandler),
    ('/admin/organizations', AdminOrgIndexHandler.AdminOrgIndexHandler),
    ('/admin/records', AdminRecordHandler.AdminRecordHandler),
    ('/admin/records/([^/]+)', AdminViewRecordHandler.AdminViewRecordHandler),
    ('/admin/organizations/new', AdminOrgNewHandler.AdminOrgNewHandler),
    ('/organizations/([^/]+)/edit', AdminOrgEditHandler.AdminOrgEditHandler),
    ('/organizations/([^/]+)/delete', AdminOrgDeleteHandler.AdminOrgDeleteHandler),
    ('/admin/organizations/dashboard', AdminOrgDashboardHandler.AdminOrgDashboardHandler),
    ('/admin/programs', AdminProgramIndexHandler.AdminProgramIndexHandler),
    ('/admin/programs/new', AdminProgramNewHandler.AdminProgramNewHandler),
    ('/programs/([^/]+)/edit', AdminProgramEditHandler.AdminProgramEditHandler),
    ('/programs/([^/]+)/delete', AdminProgramDeleteHandler.AdminProgramDeleteHandler),
    ('/admin/programs/dashboard', AdminProgramDashboardHandler.AdminProgramDashboardHandler),
    ('/admin/services', AdminServiceIndexHandler.AdminServiceIndexHandler),
    ('/admin/services/new', AdminServiceNewHandler.AdminServiceNewHandler),
    ('/services/([^/]+)/edit', AdminServiceEditHandler.AdminServiceEditHandler),
    ('/services/([^/]+)/delete', AdminServiceDeleteHandler.AdminServiceDeleteHandler),
    ('/admin/services/dashboard', AdminServiceDashboardHandler.AdminServiceDashboardHandler),
    ('/users/([^/]+)/edit', EditHandler.EditHandler),
    ('/records/([^/]+)', RecordHandler.RecordHandler),
    ('/users/([^/]+)/delete', DeleteHandler.DeleteHandler),
    ('/users/login', LoginHandler.LoginHandler),
    ('/users/logout', LogoutHandler.LogoutHandler),
    ('/users/profile', ProfileHandler.ProfileHandler),
    ('/users/reset_password', ResetPasswordHandler.ResetPasswordHandler),
    ('/users/set_password/([^/]+)', SetPasswordHandler.SetPasswordHandler),
    ('/language', LanguageHandler.LanguageHandler),
    ('/records/([^/]+)/edit', EditRecordHandler.EditRecordHandler),


    #('/api/users/login', ApiLoginHandler.ApiLoginHandler),

], config=config, debug=True)

app.error_handlers[404] = handle_404
#app.error_handlers[500] = handle_500
