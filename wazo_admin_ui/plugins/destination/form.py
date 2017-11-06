# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import StringField, SelectField, FormField, BooleanField
from wtforms.fields.html5 import IntegerField, EmailField
from wtforms.validators import InputRequired, Length, NumberRange, Regexp

from wazo_admin_ui.helpers.form import BaseForm
from wazo_admin_ui.helpers.destination import BaseDestinationForm


class HangupCongestionDestination(BaseForm):

    timeout = IntegerField(l_('Timeout'), [NumberRange(min=0)])


class HangupBusyDestination(BaseForm):

    timeout = IntegerField(l_('Timeout'), [NumberRange(min=0)])


class HangupNormalDestination(BaseForm):
    pass


class HangupDestination(BaseDestinationForm):
    select_field = 'cause'

    cause = SelectField(l_('Cause'), choices=[('normal', l_('Normal')),
                                              ('busy', l_('Busy')),
                                              ('congestion', l_('Congestion'))])
    busy = FormField(HangupBusyDestination)
    congestion = FormField(HangupBusyDestination)
    normal = FormField(HangupNormalDestination)


class ApplicationCallBackDISADestination(BaseForm):

    pin = StringField(l_('PIN'),
                      [Length(max=40), Regexp(r'^[0-9]+$')],
                      render_kw={'type': 'password'})
    context = StringField(l_('Context'), [InputRequired(), Length(max=39), Regexp(r'^[a-zA-Z0-9_-]+$')])


class ApplicationDISADestination(ApplicationCallBackDISADestination):
    pass


class ApplicationDirectoryDestination(BaseForm):

    context = StringField(l_('Context'), [InputRequired(), Length(max=39), Regexp(r'^[a-zA-Z0-9_-]+$')])


class ApplicationFaxToMailDestination(BaseForm):

    email = EmailField(l_('Email'), [InputRequired(), Length(max=80)])


class ApplicationVoicemailDestination(BaseForm):

    context = StringField(l_('Context'), [InputRequired(), Length(max=39), Regexp(r'^[a-zA-Z0-9_-]+$')])


class ApplicationDestination(BaseDestinationForm):
    select_field = 'application'

    application = SelectField(l_('Application'), choices=[('callback_disa', l_('CallBack DISA')),
                                                          ('directory', l_('Directory')),
                                                          ('disa', l_('DISA')),
                                                          ('fax_to_mail', l_('Fax To Mail')),
                                                          ('voicemail', l_('Voicemail'))])
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

    filename = StringField(l_('Filename'), [InputRequired(), Length(max=255)])
    skip = BooleanField(l_('Skip'))
    no_answer = BooleanField(l_('No Answer'))
