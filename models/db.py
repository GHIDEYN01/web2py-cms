# -*- coding: utf-8 -*- 
"""
Copyright (c) 2011 Lucas D'Avila - email lucassdvl@gmail.com / twitter @lucadavila

This file is part of web2py-cms.

web2py-cms is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License (LGPL v3) as published by
the Free Software Foundation, on version 3 of the License.

web2py-cms is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with web2py-cms.  If not, see <http://www.gnu.org/licenses/>.
"""

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:                                 # if running on Google App Engine
    db = DAL('gae://web2py_cms')                                        # connect to Google BigTable
    session.connect(request, response, db = db)                    # and store sessions and tickets there

    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                                              # else use a normal relational database
    db = DAL('sqlite://web2py_cms.sqlite')                              # if not, use SQLite or other DB

## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

# If the application is not running in an environment GAE (Google App Engine),
# then use an SMTP server or conventional logging. 
# Otherwise, use the standard used in the GAE.
if not request.env.web2py_runtime_gae:
    # mail.settings.server = 'logging'
    mail.settings.server = 'smtp.email.com'
    mail.settings.tls = True
    mail.settings.login = 'youremail@site.com:pass'
else:
    mail.settings.server = 'gae'

###########################################################################
##
## Setting the administrator to receive email notifications of CMS.
##
###########################################################################
mail.settings.sender = config.admin_email


###########################################################################
##
## Setting the configurations for module Auth.
##
###########################################################################
auth.settings.hmac_key = 'sha512:09b3128b-337c-43ae-9f04-181b948a7004'   # before define_tables()
auth.settings.mailer = mail                                              # for user email verification
auth.settings.registration_requires_verification = False                 #TODO pegar do config
auth.settings.registration_requires_approval = False                     #TODO pegar do config
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'                        #TODO pegar do config
auth.settings.reset_password_requires_verification = True                #TODO pegar do config
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'                    #TODO pegar do config

def is_author():
    """Checks whether the user is the type author."""

    return auth.has_membership(role='author', user_id = auth.user_id)
auth.is_author = is_author

def is_admin():
    """Checks whether the user is administrator type."""

    return auth.has_membership(role='admin', user_id = auth.user_id)
auth.is_admin = is_admin

#########################################################################
## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
# from gluon.contrib.login_methods.rpx_account import RPXAccount
# auth.settings.actions_disabled=['register','change_password','request_reset_password']
# auth.settings.login_form = RPXAccount(request, api_key='...',domain='...',
#    url = "http://localhost:8000/%s/default/user/login" % request.application)
## other login methods are in gluon/contrib/login_methods
#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

#TODO alterar referencias a estas variaveis para o objeto config
BLOG_NAME = config.blog_name
CONTACT_EMAIL = config.admin_email
ADMIN_EMAIL = CONTACT_EMAIL 
URL_INDEX_PAGE = URL(c='default', f='index')


#########################################################################
## Table Auth User
##   Table that stores user data.
#########################################################################
auth.settings.table_user_name = 'auth_user'
t_user = db.define_table(auth.settings.table_user_name,
    Field('first_name', length=128, default=''),
    Field('last_name', length=128, default=''),
    Field('site', default=''),
    Field('email', length=128, default='', unique=True),
    Field('password', 'password', length=512,readable=False, label='Password'),
    Field('birth_date', 'date'),
    Field('registration_key', length=512, writable=False, readable=False, default=''),
    Field('reset_password_key', length=512, writable=False, readable=False, default=''),
    Field('registration_id', length=512, writable=False, readable=False, default=''),)

# Creating user tables, use email as login
auth.define_tables(username=False)


#########################################################################
## Table Config
##   Stores system settings such as:
##
##     - Blog Name;
##     - Email Administrator;
##     -
##     - Approval for Comments;
##     - Enable / Disable contact page;
##     - Enable / Disable Login menu;
##     - Enable / Disable user registration;
##     - Favicon cms;
##     - CSS mobile interface;
##     - CSS cms;
#########################################################################
t_config = db.define_table('config',
    Field('blog_name', default = 'Bloog'),
    Field('admin_email'),
    Field('email_new_comments', 'boolean', default=True, label='Email notification for new comments'),
    Field('comments_require_approval', 'boolean', default=True),
    Field('enable_contact_page', 'boolean', default=True),    
    Field('show_menu_login', 'boolean', default='True'),
    Field('allow_user_registration', 'boolean', default=True),
    Field('favicon', 'upload'),
    Field('mobile_css', 'text', default=""),
    Field('css', 'text', default=""))
config = get_config(config_table = t_config)


###########################################################################
##
## Table Menu
##   Setting the menu list and link.
##
###########################################################################
t_menu = db.define_table('menu',
    Field('name'),
    Field('link_to', default=''),)


###########################################################################
##
## Table Page
##   Storing the pages.
##
###########################################################################
t_page = db.define_table('page',
    Field('url', label='URL (%s/your_url)'%URL(c='pages', f='read'), default="/myurl"),
    Field('use_default_layout', 'boolean', default = True),
    Field('title'),
    Field('body', 'text'),)


###########################################################################
##
## Table Ppst
##   Storing the posts for blog.
##
###########################################################################
t_post = db.define_table('post',
    Field('title', default = ''),
    Field('post', 'text'),
    Field('posted_by', t_user, default = auth.user_id),
    Field('datetime', 'datetime', label='Post date', default = request.now),
    Field('permalink'))


###########################################################################
##
## Table Comments
##   Storing the comments.
##
###########################################################################
t_post_comment = db.define_table('post_comment',
    Field('post', t_post),
    Field('unregistered_user_name', label=T('Your name')),
    Field('unregistered_user_email', label=T('Your email')),
    Field('unregistered_user_site', label=T('Your site'), default=''),
    Field('comment', 'text'),
    Field('commented_by', t_user, default = auth.user_id),
    Field('datetime', 'datetime', label='Comment date', default = request.now),
    Field('status', default='W' if config.comments_require_approval else 'A'))
