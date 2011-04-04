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

pygravatar_gravatar = local_import('pygravatar.gravatar', reload = False)
Gravatar = pygravatar_gravatar.Gravatar

def get_config(config_table):
    return config_table._db(t_config.id>0).select().first() or config_table.insert()


def get_confirmation_user(back, next, message='Confirm this ?', positive_option = 'Yes', negative_option = 'No'):
    redirect(URL(c='default', f='dialog', args='confirm', vars=dict(back = back, next = next, message = message, positive_option = positive_option, negative_option = negative_option)))


def get_external_url(s_url):
    if s_url is None:
        return ''
    elif not s_url.startswith('http'):
        return 'http://%s'%s_url
    return s_url


def get_full_url_page(page, default='#'):
    return URL(c='default', f='pages')+page.url or default


def get_last_posts():
    return t_post._db(t_post.id>0).select(t_post.id, t_post.title, t_post.permalink, orderby=~t_post.datetime, limitby=(0,10))

def __give_permission(role, user_id):
    if not auth.id_group(role=role):    
        auth.add_group(role=role)    
    auth.add_membership(role=role, user_id=user_id)
    
