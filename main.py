import webapp2
import jinja2
import os
from webapp2_extras import routes
from models import Commune
from handlers.static_pages import ViewServiceHandler, PublicExportHandler, AboutHandler, ContactHandler, MainHandler, SearchHandler, ServicesHandler, SuggestServicesHandler, ManualHandler, RecordHandler, LanguageHandler, PublicRecordHandler
from handlers.admin import AdminServiceViewHandler, SearchRecordHandler, IndexHandler, UsersIndexHandler, NewUserHandler, EmailEndpointHandler, DashboardHandler, DashboardItemHandler, UserDashboardHandler, UserDashboardItemHandler, AdminIFormBuilderHandler, AdminRecordHandler, AdminViewRecordHandler, EditRecordHandler, NewServiceHandler, NewProgramHandler, NewRecordHandler, ExportHandler
from handlers.users import EditHandler, LoginHandler, LogoutHandler, ProfileHandler, ResetPasswordHandler, SetPasswordHandler, DeleteHandler
from handlers.api.users import ApiLoginHandler
from handlers.admin.organizations import AdminOrgIndexHandler, AdminOrgNewHandler, AdminOrgEditHandler, AdminOrgDeleteHandler, AdminOrgDashboardHandler
from handlers.admin.programs import AdminProgramIndexHandler, AdminProgramNewHandler, AdminProgramEditHandler, AdminProgramDeleteHandler, AdminProgramDashboardHandler
from handlers.admin.services import AdminServiceIndexHandler, AdminServiceNewHandler, AdminServiceEditHandler, AdminServiceDeleteHandler, AdminServiceDashboardHandler
from handlers.schema_updates import UpdateHandler
from handlers.site_test import SiteTest

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'LK@#J$LK@#J$@#IUR(E*R)WE(FIUAFOJOWE%IUQ#)(%*TU$OIJQTJRWKGUWRE(T*W)$#(*%W$#%OIJRWOIEUWR"0t9*',
}



class Route(routes.RedirectRoute):
  def __init__(self, *args, **kwargs):
    # This causes a URL to redirect to its canonical version without a slash.
    # See http://webapp-improved.appspot.com/api/webapp2_extras/routes.html#webapp2_extras.routes.RedirectRoute
    if 'strict_slash' not in kwargs:
      kwargs['strict_slash'] = True
    routes.RedirectRoute.__init__(self, *args, **kwargs)

def handle_404(request, response, exception):
    response.write('Page not found')
    response.set_status(404)

def handle_500(request, response, exception):
    response.write('Oops! I could swear this page was here!')
    response.set_status(500)

app = webapp2.WSGIApplication([
    (r'/', MainHandler.MainHandler, "home"),
    (r'/about', AboutHandler.AboutHandler, "about"),
    (r'/search', SearchHandler.SearchHandler, "search"),
    (r'/contact', ContactHandler.ContactHandler, "contact"),
    (r'/suggest_services', SuggestServicesHandler.SuggestServicesHandler, "suggest_services"),
    (r'/mental_illness_services', ServicesHandler.ServicesHandler, "mental_illness_services"),
    (r'/manual', ManualHandler.ManualHandler, "manual"),
    (r'/admin', IndexHandler.IndexHandler, "admin"),
    #('/admin/iformbuilder_task', AdminIFormBuilderHandler.AdminIFormBuilderHandler),
    (r'/admin/searches', SearchRecordHandler.SearchRecordHandler, "admin_searches"),
    (r'/admin/users', UsersIndexHandler.UsersIndexHandler, "admin_users"),
    (r'/admin/users/new', NewUserHandler.NewUserHandler, "admin_users_new" ),
    (r'/admin/users/dashboard', UserDashboardHandler.UserDashboardHandler, "admin_user_dashboard"),
    (r'/admin/users_dashboard/([^/]+)', UserDashboardItemHandler.UserDashboardItemHandler, "admin_user_dashboard_item"),
    (r'/admin/users/([^/]+)', EmailEndpointHandler.EmailEndpointHandler, "users_item"),
    (r'/admin/dashboard', DashboardHandler.DashboardHandler, "admin_dashboard"),
    (r'/admin/dashboard/([^/]+)', DashboardItemHandler.DashboardItemHandler, "admin_dashboard_item"),
    # ('/admin/organizations', AdminOrgIndexHandler.AdminOrgIndexHandler),
    (r'/admin/records', AdminRecordHandler.AdminRecordHandler, "admin_records"),
    (r'/admin/records/([^/]+)', AdminViewRecordHandler.AdminViewRecordHandler, "admin_records_item"),
    # ('/admin/organizations/new', AdminOrgNewHandler.AdminOrgNewHandler),
    # ('/organizations/([^/]+)/edit', AdminOrgEditHandler.AdminOrgEditHandler),
    # ('/organizations/([^/]+)/delete', AdminOrgDeleteHandler.AdminOrgDeleteHandler),
    # ('/admin/organizations/dashboard', AdminOrgDashboardHandler.AdminOrgDashboardHandler),
    (r'/admin/programs', AdminProgramIndexHandler.AdminProgramIndexHandler, "admin_programs"),
    (r'/admin/programs/new', AdminProgramNewHandler.AdminProgramNewHandler, "admin_programs_new"),
    (r'/programs/([^/]+)/edit', AdminProgramEditHandler.AdminProgramEditHandler, "programs_edit"),
    (r'/programs/([^/]+)/delete', AdminProgramDeleteHandler.AdminProgramDeleteHandler, "programs_delete"),
    (r'/admin/programs/dashboard', AdminProgramDashboardHandler.AdminProgramDashboardHandler, "programs_dashboard"),
    # ('/admin/services', AdminServiceIndexHandler.AdminServiceIndexHandler),
    (r'/admin/services/([^/]+)', AdminServiceViewHandler.AdminServiceViewHandler, "admin_service_view"),
    # ('/admin/services/new', AdminServiceNewHandler.AdminServiceNewHandler),
    ('/services/([^/]+)/edit', AdminServiceEditHandler.AdminServiceEditHandler),
    # ('/services/([^/]+)/delete', AdminServiceDeleteHandler.AdminServiceDeleteHandler),
    # ('/admin/services/dashboard', AdminServiceDashboardHandler.AdminServiceDashboardHandler),
    (r'/users/([^/]+)/edit', EditHandler.EditHandler, "users_edit"),
    (r'/records/new', NewRecordHandler.NewRecordHandler, "records_new"),
    (r'/programs/new', NewProgramHandler.NewProgramHandler, "programs_new"),
    (r'/services/new', NewServiceHandler.NewServiceHandler, "services_new"),
    (r'/services/([^/]+)', ViewServiceHandler.ViewServiceHandler, "services_view"),
    # ('/records/([^/]+)', RecordHandler.RecordHandler),
    (r'/users/([^/]+)/delete', DeleteHandler.DeleteHandler, "users_delete"),
    (r'/users/login', LoginHandler.LoginHandler, "users_login"),
    (r'/users/logout', LogoutHandler.LogoutHandler, "users_logout"),
    (r'/users/profile', ProfileHandler.ProfileHandler, "users_profile"),
    (r'/users/reset_password', ResetPasswordHandler.ResetPasswordHandler, "users_reset_password"),
    (r'/users/set_password/([^/]+)', SetPasswordHandler.SetPasswordHandler, "users_set_password"),
    (r'/language', LanguageHandler.LanguageHandler, "language"),
    (r'/records/([^/]+)/edit', EditRecordHandler.EditRecordHandler, "records_edit"),
    (r'/update_handler', UpdateHandler.UpdateHandler, "update_handler"),
    (r'/admin/export/([^/]+)', ExportHandler.ExportHandler, "admin_export_csv"),
    (r'/isitlive', SiteTest.SiteTest, "isitlive"),
    (r"/records/([^/]+)", PublicRecordHandler.PublicRecordHandler, "records_view"),
    (r"/export/([^/]+)", PublicExportHandler.PublicExportHandler, "public_export_handler")



    #('/api/users/login', ApiLoginHandler.ApiLoginHandler),

], config=config, debug=True)

app.error_handlers[404] = handle_404
#app.error_handlers[500] = handle_500
