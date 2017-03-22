# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wtforms.fields import HiddenField


class CustomHiddenField(HiddenField):

    def __init__(self, *args, **kwargs):
        def remove_none(value):
            return value or ''
        super(CustomHiddenField, self).__init__(filters=[remove_none], *args, **kwargs)
