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

response.title = request.application
response.subtitle = T('customize me!')

#http://dev.w3.org/html5/markup/meta.name.html 
response.meta.author = 'you'
response.meta.description = 'Free and open source full-stack enterprise framework for agile development of fast, scalable, secure and portable database-driven web-based applications. Written and programmable in Python'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Enterprise Framework'
response.meta.copyright = "Copyright Lucas D'Avila 2011"


for m in t_menu._db(t_menu.id>0).select():
    response.menu+=[
        (m.name, False, m.link_to, []),
        ]

if config.enable_contact_page:
    response.menu += [(T('contact'), False, URL(c='default', f='contact'), []),]

if auth.is_author():
    response.menu += [('dashboard', False, URL(c='default', f='dashboard'), []),]

if auth.is_logged_in():
    response.menu += [('logout', False, URL(c='default', f='user', args='logout'), []),]
elif config.show_menu_login:
    response.menu += [('login', False, URL(c='default', f='user', args='login'), []),]
