# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import requests

from flask_babel import lazy_gettext as l_
from flask_wtf import FlaskForm
from requests.exceptions import HTTPError
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError

from wazo_admin_ui.core.auth import AuthClient
from wazo_admin_ui.core.user import UserUI


USERNAME_PASSWORD_ERROR = l_('Wrong username and/or password')


def unauthorized(error):
    return error.response is not None and error.response.status_code == 401


class LoginForm(FlaskForm):

    username = StringField(l_('Username'), validators=[InputRequired()])
    password = PasswordField(l_('Password'), validators=[InputRequired()])
    submit = SubmitField(l_('Login'))

    def validate(self):
        super(LoginForm, self).validate()
        try:
            response = AuthClient(username=self.username.data,
                                  password=self.password.data).token.new('xivo_admin', expiration=3600)
        except HTTPError as e:
            if unauthorized(e):
                self.username.errors.append(USERNAME_PASSWORD_ERROR)
                self.password.errors.append(USERNAME_PASSWORD_ERROR)
                return False
            raise ValidationError(l_('Error with Wazo authentication server: %(error)s', error=e.message))
        except requests.ConnectionError:
            raise ValidationError(l_('Wazo authentication server connection error'))

        self.user = UserUI(response['token'], response['auth_id'])

        return True
