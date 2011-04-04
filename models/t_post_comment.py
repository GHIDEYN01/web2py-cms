# -*- coding: utf-8 -*- 
"""
Copyright (c) 2011 Lucas D'Avila - email lucassdvl@gmail.com / twitter @lucadavila

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

#crud table post
crud_post_comment = Crud(globals(),db)
crud_post_comment.settings.auth = None
crud_post_comment.settings.create_next = URL(f='post', args=request.args)
crud_post_comment.settings.update_next = URL(f='post', args=request.args)
crud_post_comment.settings.delete_next = URL(f='post', args=request.args)

crud_post_comment.messages.submit_button = T('Comment')
crud_post_comment.messages.record_created = T('Yep! commented') if not config.comments_require_approval else T('Yep! commented, Your comment will appear after approval')
crud_post_comment.messages.record_updated = T('Comment Updated')

#restrictions
t_post_comment.comment.requires = IS_NOT_EMPTY(error_message=T('Ops! falta seu comentário.'))
if not auth.is_logged_in():
    t_post_comment.unregistered_user_name.requires = IS_NOT_EMPTY(error_message=T('Ops! Qual seu nome ?'))
    t_post_comment.unregistered_user_email.requires = IS_EMAIL(error_message=T('Ops! Qual seu email ?'))
t_post_comment.unregistered_user_site.requires = IS_EMPTY_OR(IS_URL(error_message='Ops! informe um endereço de site correto'))
t_post_comment.commented_by.requires = IS_IN_DB(db, t_user.id, '%(first_name)s')
t_post_comment.datetime.requires = IS_DATETIME()
t_post_comment.status.requires = IS_IN_SET(['W', 'A', 'S'])#W - waiting approval, A - approved, S - SPAM

t_post_comment.post.writable = False
t_post_comment.post.readable = False
t_post_comment.commented_by.writable = False
t_post_comment.commented_by.readable = False
t_post_comment.datetime.writable = False
t_post_comment.datetime.readable = False
t_post_comment.status.writable = False
t_post_comment.status.readable = False

if auth.is_logged_in():
    t_post_comment.unregistered_user_name.readable = False
    t_post_comment.unregistered_user_name.writable = False
    t_post_comment.unregistered_user_email.readable = False
    t_post_comment.unregistered_user_email.writable = False
    t_post_comment.unregistered_user_site.readable = False
    t_post_comment.unregistered_user_site.writable = False
