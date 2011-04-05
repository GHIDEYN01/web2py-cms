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
crud_config = Crud(globals(),db)
crud_config.settings.auth = None
crud_config.settings.update_next = URL(f='dashboard')

#restrictions

t_config.blog_name.requires = IS_NOT_EMPTY()
t_config.admin_email.requires = IS_EMPTY_OR(IS_EMAIL())
