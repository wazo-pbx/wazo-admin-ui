# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


class UserUI(object):

    def __init__(self, token, uuid=None):
        self._token = token
        self.uuid = uuid

    def get_id(self):
        return self._token

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
