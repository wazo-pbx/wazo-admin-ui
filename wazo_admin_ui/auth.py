# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_auth_client import Client


class AuthClient(Client):
    _auth_config = None

    def __init__(self, **config):
        config.update(self._auth_config)
        super(AuthClient, self).__init__(**config)

    @classmethod
    def set_config(cls, auth_config):
        cls._auth_config = auth_config
