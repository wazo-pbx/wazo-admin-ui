# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import Flask, jsonify

app = Flask(__name__)

context = ('/usr/local/share/ssl/auth/server.crt', '/usr/local/share/ssl/auth/server.key')


@app.route('/0.1/token', methods=['POST'])
def create_token():
    return jsonify({'data': {'token': 'the-token',
                             'auth_id': 'the-auth-id'}})


@app.route('/0.1/token/<id>', methods=['HEAD'])
def head_token(id):
    return '', 204


@app.route('/0.1/token/<id>', methods=['GET'])
def get_token(id):
    return jsonify({'data': {'token': id,
                             'auth_id': 'the-auth-id'}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9497, ssl_context=context, debug=True)
