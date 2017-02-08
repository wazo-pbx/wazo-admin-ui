# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from requests.exceptions import HTTPError
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError

from wazo_admin_ui.core.auth import AuthClient
from wazo_admin_ui.core.user import UserUI


USERNAME_PASSWORD_ERROR = lazy_gettext('Wrong username and/or password')


def unauthorized(error):
    return error.response is not None and error.response.status_code == 401


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

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
            raise ValidationError('Error with Wazo authentication server: {}:'.format(e.message))

        self.user = UserUI(response['token'], response['auth_id'])

        return True
