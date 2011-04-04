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
crud_page = Crud(globals(),db)
crud_page.settings.auth = None
crud_page.settings.create_next = URL(f='customize')
crud_page.settings.update_next = URL(f='customize')
crud_page.settings.delete_next = URL(f='customize')

#restrictions
t_page.url.requires = IS_URL(error_message='enter a valid URL ex: /myurl')#IS_ALPHANUMERIC(error_message=T('must be alphanumeric!'))]
t_page.title.requires = IS_NOT_EMPTY()
t_page.body.requires = IS_NOT_EMPTY()
