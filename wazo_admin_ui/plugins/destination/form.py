# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wtforms.fields import StringField, SelectField, FormField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, NumberRange

from wazo_admin_ui.helpers.form import BaseForm
from wazo_admin_ui.helpers.destination import BaseDestinationForm


class HangupCongestionDestination(BaseForm):

    timeout = IntegerField('Timeout', [NumberRange(min=0)])


class HangupBusyDestination(BaseForm):

    timeout = IntegerField('Timeout', [NumberRange(min=0)])


class HangupNormalDestination(BaseForm):
    pass


class HangupDestination(BaseDestinationForm):
    select_field = 'cause'

    cause = SelectField('Cause', choices=[('normal', 'Normal'), ('busy', 'Busy'), ('congestion', 'Congestion')])
    busy = FormField(HangupBusyDestination)
    congestion = FormField(HangupBusyDestination)
    normal = FormField(HangupNormalDestination)


class CustomDestination(BaseForm):

    command = StringField(validators=[InputRequired(), Length(max=255)])


class NoneDestination(BaseForm):
    pass
