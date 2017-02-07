# -*- coding: utf-8 -*-
# Copyright 2017 by Sylvain Boily
# SPDX-License-Identifier: GPL-3.0+

from flask import Blueprint
from flask_menu.classy import register_flaskview

from .resource import Conferences

conference = Blueprint('conference', __name__, template_folder='templates',
                       static_folder='static', static_url_path='/%s' % __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        config = dependencies['config']

        Conferences.register(conference, route_base='/conferences', route_prefix='')
        register_flaskview(conference, Conferences)

        core.register_blueprint(conference)
