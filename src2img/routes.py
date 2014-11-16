import PyV8
import logging
import codecs
import json
import os
from flask import jsonify, request, abort, session
from .helpers import Helpers
from .renderer import BemhtmlRenderer

log = logging.getLogger('src2img')

BEMJSON_KEY = 'bem.json'
BEMHTML_KEY = 'bemhtml.js'


class Routes(object):

    protected_methods = ['PUT']

    def __init__(self, flask, app):
        self._fl = flask
        self.app = app

        assets = app.config.get('global', 'assets')
        self.assets = {}
        for root, dirs, files in os.walk(assets):
            for f in files:
                with codecs.open(os.path.join(root, f), encoding='utf-8') as fd:
                    name = f.split(os.path.extsep)[0]
                    if name not in self.assets:
                        self.assets[name] = {}

                    key = None
                    if f.endswith(BEMJSON_KEY):
                        key = BEMJSON_KEY
                    elif f.endswith(BEMHTML_KEY):
                        key = BEMHTML_KEY

                    if key is not None:
                        self.assets[name][key] = fd.read()

    def setup(self):
        fl = self._fl
        index_renderer = BemhtmlRenderer.start(
            self.assets['index'][BEMHTML_KEY])

        def generate_csrf():
            if '_csrf_token' not in session:
                session['_csrf_token'] = Helpers.random_token()
            return session['_csrf_token']

        @fl.before_request
        def csrf_protect():
            if request.method in self.protected_methods:
                token = session.pop('_csrf_token', None)
                if not token or token != request.form.get('_csrf_token'):
                    abort(400)
                    return

        @fl.route('/', methods=['GET'])
        def index():
            return renderer.ask({
                'bemjson': self.assets['index'][BEMJSON_KEY],
                'gc': True,
                'params': {'csrf': generate_csrf()}
            })

        @fl.route('/image/put', methods=['PUT'])
        def put_image():
            log.info(
                'Saving image from {0}'.format(request.remote_addr))
            data = request.form.get('image', None)
            if data is None:
                abort(400)
                return

            return jsonify({})

        @fl.route('/image/get/<ident>', methods=['GET'])
        def get_image(ident):
            return jsonify({})
