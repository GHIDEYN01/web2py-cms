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

#crud table post
crud_menu = Crud(globals(),db)
crud_menu.settings.auth = None
crud_menu.settings.create_next = URL(f='customize')
crud_menu.settings.update_next = URL(f='customize')
crud_menu.settings.delete_next = URL(f='customize')

#restrictions
t_menu.name.requires = IS_NOT_EMPTY()
t_menu.link_to.requires = IS_EMPTY_OR(IS_URL())
