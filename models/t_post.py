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
crud_post = Crud(globals(),db)
crud_post.settings.auth = None
crud_post.settings.create_next = URL(f='index')
crud_post.settings.update_next = URL(f='post', args=request.args[1:])
crud_post.settings.delete_next = URL(f='index')

#restrictions
t_post.post.requires = IS_NOT_EMPTY()
t_post.posted_by.requires = IS_IN_DB(db, t_user.id, '%(first_name)s')
t_post.datetime.requires = IS_DATETIME()

t_post.posted_by.writable = False
t_post.permalink.writable = False
t_post.permalink.readable = False


def set_permalink(post_id):
    """Retorna o perma link para os posts
    """
    import string
    safe = string.ascii_letters + string.digits + '_-'
    post = t_post[post_id]
    title = ''.join([char if char in safe else '' for char in post.title]).lower() if post.title else post.id
    if post: post.update_record(permalink='%s/%s/%s/%s'%(post.datetime.year, post.datetime.month, post.datetime.day, title))


def get_permalink(args):
    if len(args) < 4: redirect(URL_INDEX_PAGE)
    return '%s/%s/%s/%s'%(args[0],args[1],args[2],args[3],)


def get_post(args):
    return t_post._db(t_post.permalink==get_permalink(args=args)).select().first()
    
