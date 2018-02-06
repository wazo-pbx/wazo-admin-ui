# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, FormField, FieldList


class BaseForm(FlaskForm):

    def to_dict(self, empty_string=False):
        result = {}
        for name, f in self._fields.items():
            if name == 'csrf_token' or isinstance(f, SubmitField):
                continue
            elif isinstance(f, FormField):
                result[name] = f.form.to_dict()
            elif isinstance(f, FieldList):
                result[name] = [entry.to_dict() for entry in f.entries]
            elif not f.raw_data and f.default is None:
                continue
            else:
                default = f.default or f.data
                data = f.data if f.data else default
                result[name] = data if empty_string or data != '' else None
        return result

    def populate_errors(self, resource):
        for form_name, form_value in self._fields.items():
            if form_name not in resource:
                continue

            if isinstance(form_value, FormField):
                form_value.form.populate_errors(resource[form_name])
            elif isinstance(form_value, FieldList):
                for index, form in enumerate(form_value.entries):
                    form.populate_errors(resource[form_name].get(str(index), {}))
            else:
                # normally it's form.validate() that make this conversion
                form_value.errors = list(form_value.errors)

                form_value.errors.append(resource[form_name])
