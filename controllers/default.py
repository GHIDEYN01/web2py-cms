# -*- coding: utf-8 -*- 
"""
Copyright (c) 2011 Lucas D'Avila - email <lucassdvl@gmail.com> / twitter @lucadavila

This file is part of bloog.

bloog is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License (LGPL v3) as published by
the Free Software Foundation, on version 3 of the License.

bloog is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with bloog.  If not, see <http://www.gnu.org/licenses/>.
"""

def index():
    posts = t_post._db(t_post.id>0).select(orderby=~t_post.datetime)
    return dict(posts = posts)

def post():
    post = get_post(args = request.args) or redirect(URL_INDEX_PAGE)
    t_post_comment.post.default = post.id
    if auth.is_logged_in():
        t_post_comment.commented_by.default = auth.user_id
    crud_post_comment.settings.formstyle='divs'
    crud_post_comment.settings.create_onaccept = lambda form_c:mail.send(to=config.admin_email, subject=T('New comment on post %s')%post.title, message='Comment: %s '%form_c.vars.comment)
    form_new_comment = crud_post_comment.create(t_post_comment)
    comments = post.post_comment.select()
    return dict(post=post, comments = comments, form_new_comment = form_new_comment)


def contact():
    if not config.enable_contact_page:
        session.flash('Ops! contact page is not enabled :(')
        redirect(URL_INDEX_PAGE)
    else:
        form = FORM(TABLE(
            TR(
                TD(T('Your name:')),
                TD(INPUT(_name='name', requires=IS_NOT_EMPTY(error_message=T('Please enter your name')))),
            ),
            TR(
                TD(T('Your email:')),
                TD(INPUT(_name='email', requires=IS_EMAIL(error_message=T('Please enter your email')))),
            ),
            TR(
                TD(T('Message:')),
                TD(TEXTAREA(_name='message', requires=IS_NOT_EMPTY(error_message=T('Please enter your message')))),
            ),
            TR(
                TD(),
                TD(INPUT(_type='submit', _value=T('Send'))))))

        if form.accepts(request.vars, session):
            data = dict(app = BLOG_NAME, name = form.vars.name, email = form.vars.email, message = form.vars.message)
            message = T('Hello!\n\n%(name)s (email: %(email)s) sent a message to you, through the contact page of'+ \
                        ' the site %(app)s\nmessage:%(message)s')%data
            if mail.send(to=CONTACT_EMAIL, subject='Contact message %s'%BLOG_NAME,message=message):
                session.flash=T('Thank you, message sent.')
                redirect(URL_INDEX_PAGE)
            else:
                response.flash=T('Ops! We cannot send your message :(, please try again later.')    
    return dict(form = form)

def user():
    if not t_user._db(t_user.id>0).select().first():
        auth.settings.register_onaccept.append(lambda auth_form:__give_permission(role='admin', user_id=auth_form.vars.id))
        auth.settings.register_onaccept.append(lambda auth_form:__give_permission(role='author', user_id=auth_form.vars.id))
    return dict(form = auth())


@auth.requires_membership('admin')
def manage():
    arg = request.args(0)
    if arg == 'users':
        authors = None #TODO select usuários com papel author
        admins = None #TODO select usuários com papel admin
        users = None #TODO select usuários sem papel author e admin
        return dict(authors = authors, admins = admins, users = users)
    


@auth.requires_membership('author')
def dashboard():
    return {}


@auth.requires_membership('admin')
def customize():
    form_config = crud_config.update(t_config, config, deletable  = False)
    menus = t_menu._db(t_menu.id>0).select()
    pages = t_page._db(t_page.id>0).select()
    return dict(form_config = form_config, menus = menus, pages = pages)

#def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
#    return response.download(request,db)


@auth.requires_membership('author')
def new():

    t_post.posted_by.readable = False
    form = crud_post.create(t_post, onaccept=lambda form:set_permalink(form.vars.id))
#    if form.accepts(request.vars, session):
#        set_permalink(form.vars.id)
#        redirect(crud_post.settings.create_next)
    return dict(form = form)


@auth.requires_membership('author')
def edit():
    arg = request.args(0)
    if arg == 'post':
        post = get_post(args = request.args[1:])    
        t_post.posted_by.readable = False
        form = crud_post.update(t_post, post)
        return dict(form = form)    
    elif arg == 'comment':    
        comment_id = request.args(1) or redirect(URL_INDEX_PAGE)
        new_status = request.vars.new_status or redirect(URL_INDEX_PAGE)
        new_status = new_status.upper()
        if new_status not in ('APPROVED','SPAM'): redirect(URL_INDEX_PAGE)

        comment = t_post_comment[comment_id]
        if comment:
            comment.update_record(status = new_status[0])
            session.flash = crud_post_comment.messages.record_updated
            redirect(URL(f='post', args=comment.post.permalink))


@auth.requires_membership('author')
def delete():
    arg = request.args(0) or redirect(URL_INDEX_PAGE)
    if arg == 'comment':
        comment = t_post_comment[request.args(1)] or redirect(URL_INDEX_PAGE)
        if request.args(2) != 'yes':
            get_confirmation_user(message = 'Delete this comment ?', back=URL(f='post', args=comment.post.permalink), next=URL(args=('comment', \
                comment.id, 'yes')))
        crud_post_comment.settings.delete_next = URL(f='post', args=comment.post.permalink)
        crud_post_comment.delete(t_post_comment, comment.id)


@auth.requires_membership('admin')
def menu():
    arg = request.args(0) or redirect(URL_INDEX_PAGE)
    response.view = '%s/%s.%s'%('default', arg, request.extension)
    if arg == 'new':
        form = crud_menu.create(t_menu)
        return dict(form = form)

    elif arg == 'edit':
        menu_id = request.args(1) or redirect(URL_INDEX_PAGE)
        form = crud_menu.update(t_menu, menu_id, deletable=False)
        return dict(form = form)

    elif arg == 'delete':
        menu_id = request.args(1) or redirect(URL_INDEX_PAGE)

        if request.args(2) != 'yes':
            get_confirmation_user(message = 'Delete this menu ?', back=URL(f='customize'), next=URL(args=('delete', menu_id, 'yes')))

        crud_menu.delete(t_menu, menu_id)


@auth.requires_membership('admin')
def page():
    arg = request.args(0) or redirect(URL_INDEX_PAGE)
    response.view = '%s/%s.%s'%('default', arg, request.extension)

    if arg == 'new':
        form = crud_page.create(t_page)
        return dict(form = form)

    elif arg == 'edit':
        page_id = request.args(1) or redirect(URL_INDEX_PAGE)
        form = crud_page.update(t_page, page_id, deletable=False)
        return dict(form = form)

    elif arg == 'delete':
        page_id = request.args(1) or redirect(URL_INDEX_PAGE)

        if request.args(2) != 'yes':
            get_confirmation_user(message = 'Delete this page ?', back=URL(f='customize'), next=URL(args=('delete', page_id, 'yes')))

        crud_page.delete(t_page, page_id)

    elif arg == 'create_menu':
        page = t_page[request.args(1)] or redirect(URL_INDEX_PAGE)
        t_menu.insert(name = page.title or '?', link_to = get_full_url_page(page = page))
        t_menu._db.commit()
        redirect(URL(f='customize'))


def pages():
    page = t_page._db(t_page.url == '/%s'%request.args(0)).select().first() or redirect(URL_INDEX_PAGE)
    if not page.use_default_layout:
        response.view = '%s/%s.%s'%('default', 'pages_unstyled', request.extension)
    return dict(page = page)


def dialog():
    if request.args(0) == 'confirm':
        return {}   
