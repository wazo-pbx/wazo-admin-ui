# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import requests
from requests.exceptions import HTTPError

from flask_babel import lazy_gettext as l_
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, ValidationError

from wazo_admin_ui.auth import AuthClient
from wazo_admin_ui.user import UserUI

USERNAME_PASSWORD_ERROR = l_('Wrong username and/or password')


def unauthorized(error):
    return error.response is not None and error.response.status_code == 401


class LoginForm(FlaskForm):

    username = StringField(l_('Username'), validators=[InputRequired()])
    password = PasswordField(l_('Password'), validators=[InputRequired()])
    language = SelectField(l_('Language'))
    submit = SubmitField(l_('Login'))

    def validate(self):
        super().validate()
        try:
            response = AuthClient(username=self.username.data,
                                  password=self.password.data).token.new('xivo_admin', expiration=60 * 60 * 12)
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
