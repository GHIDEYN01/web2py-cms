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

if not config.allow_user_registration:
    auth.settings.actions_disabled+=['register']

t_user.first_name.requires = IS_NOT_EMPTY(error_message='Informe seu primeiro nome')
t_user.last_name.requires = IS_NOT_EMPTY(error_message='Informe seu último nome')
t_user.birth_date.requires = IS_EMPTY_OR(IS_DATE(error_message='Informe uma data no formato DD-MM-AAAA, ex: 1989-12-31'))
t_user.password.requires = [IS_LENGTH(minsize=6, maxsize=256, error_message = 'Informe no minimo 6 caracteres'), CRYPT()]
t_user.email.requires = [IS_EMAIL(error_message='Informe um email válido'),IS_NOT_IN_DB(t_user._db, t_user.email, error_message='Este email já foi usado em outro cadastro, informe outro email ou tente recuperar a senha')]
