# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import argparse

from xivo.chain_map import ChainMap
from xivo.config_helper import read_config_file_hierarchy
from xivo.http_helpers import DEFAULT_CIPHERS
from xivo.xivo_logging import get_log_level_by_name


_DEFAULT_CONFIG = {
    'config_file': '/etc/wazo-admin-ui/config.yml',
    'extra_config_files': '/etc/wazo-admin-ui/conf.d',
    'debug': False,
    'foreground': False,
    'log_level': 'info',
    'user': 'wazo-admin-ui',
    'log_filename': '/var/log/wazo-admin-ui.log',
    'pid_filename': '/var/run/wazo-admin-ui/wazo-admin-ui.pid',
    'session_file_dir': '/var/lib/wazo-admin-ui/sessions',
    'https': {
        'listen': '0.0.0.0',
        'port': 9296,
        'certificate': '/usr/share/xivo-certs/server.crt',
        'private_key': '/usr/share/xivo-certs/server.key',
        'ciphers': DEFAULT_CIPHERS
    },
    'auth': {
        'host': '127.0.0.1',
        'port': 9497,
        'verify_certificate': '/usr/share/xivo-certs/server.crt'
    },
    'confd': {
        'host': '127.0.0.1',
        'port': 9487,
        'verify_certificate': '/usr/share/xivo-certs/server.crt'
    },
    'enabled_plugins': {
        'admin': True,
        'authentication': True,
        'index': True,
    }
}


def _parse_cli_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--config-file',
                        action='store',
                        help='The path to the config file. Default %(default)s')
    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        help='Log debug messages. Default %(default)s')
    parser.add_argument('-f',
                        '--foreground',
                        action='store_true',
                        help="Foreground, don't daemonize. Default %(default)s")
    parser.add_argument('-l',
                        '--log-level',
                        action='store',
                        help="Logs messages with LOG_LEVEL details. Must be one of:\n"
                             "critical, error, warning, info, debug. Default: %(default)s")
    parser.add_argument('-u',
                        '--user',
                        action='store',
                        help='The owner of the process')
    parsed_args = parser.parse_args(argv)

    result = {}
    if parsed_args.config_file:
        result['config_file'] = parsed_args.config_file
    if parsed_args.debug:
        result['debug'] = parsed_args.debug
    if parsed_args.foreground:
        result['foreground'] = parsed_args.foreground
    if parsed_args.log_level:
        result['log_level'] = parsed_args.log_level
    if parsed_args.user:
        result['user'] = parsed_args.user

    return result


def _get_reinterpreted_raw_values(config):
    result = {}

    log_level = config.get('log_level')
    if log_level:
        result['log_level'] = get_log_level_by_name(log_level)

    enabled_plugins = config.get('enabled_plugins')
    if enabled_plugins:
        result['enabled_plugins'] = _extract_enabled_plugins(enabled_plugins)

    return result


def _extract_enabled_plugins(plugins):
    return [plugin for plugin, enabled in plugins.iteritems() if enabled]


def load(argv):
    cli_config = _parse_cli_args(argv)
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    reinterpreted_config = _get_reinterpreted_raw_values(ChainMap(cli_config, file_config, _DEFAULT_CONFIG))
    return ChainMap(reinterpreted_config, cli_config, file_config, _DEFAULT_CONFIG)
