# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wtforms.fields import StringField, SelectField, FormField, BooleanField
from wtforms.fields.html5 import IntegerField, EmailField
from wtforms.validators import InputRequired, Length, NumberRange, Regexp

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


class ApplicationCallBackDISADestination(BaseForm):

    pin = StringField('PIN',
                      [Length(max=40), Regexp(r'^[0-9]+$')],
                      render_kw={'type': 'password'})
    context = StringField('Context', [InputRequired(), Length(max=39), Regexp(r'^[a-zA-Z0-9_-]+$')])


class ApplicationDISADestination(ApplicationCallBackDISADestination):
    pass


class ApplicationDirectoryDestination(BaseForm):

    context = StringField('Context', [InputRequired(), Length(max=39), Regexp(r'^[a-zA-Z0-9_-]+$')])


class ApplicationFaxToMailDestination(BaseForm):

    email = EmailField('Email', [InputRequired(), Length(max=80)])


class ApplicationVoicemailDestination(BaseForm):

    context = StringField('Context', [InputRequired(), Length(max=39), Regexp(r'^[a-zA-Z0-9_-]+$')])


class ApplicationDestination(BaseDestinationForm):
    select_field = 'application'

    application = SelectField('Application', choices=[('callback_disa', 'CallBack DISA'),
                                                      ('directory', 'Directory'),
                                                      ('disa', 'DISA'),
                                                      ('fax_to_mail', 'Fax To Mail'),
                                                      ('voicemail', 'Voicemail')])
    callback_disa = FormField(ApplicationCallBackDISADestination)
    directory = FormField(ApplicationDirectoryDestination)
    disa = FormField(ApplicationDISADestination)
    fax_to_mail = FormField(ApplicationFaxToMailDestination)
    voicemail = FormField(ApplicationVoicemailDestination)


class CustomDestination(BaseForm):

    command = StringField(validators=[InputRequired(), Length(max=255)])


class NoneDestination(BaseForm):
    pass


class SoundDestination(BaseForm):

    filename = StringField('Filename', [InputRequired(), Length(max=255)])
    skip = BooleanField('Skip')
    no_answer = BooleanField('No Answer')
