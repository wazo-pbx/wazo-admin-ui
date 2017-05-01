# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wtforms.fields import StringField
from wtforms.validators import InputRequired, Length

from wazo_admin_ui.helpers.form import BaseForm


class CustomDestination(BaseForm):

    command = StringField(validators=[InputRequired(), Length(max=255)])


class NoneDestination(BaseForm):
    pass
