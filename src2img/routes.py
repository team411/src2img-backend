from flask import jsonify, request
import PyV8
import logging

log = logging.getLogger('src2img')


class Routes(object):

    def __init__(self, flask, app):
        self._fl = flask
        self.app = app

    def setup(self):
        fl = self._fl

        @fl.route('/', methods=['GET'])
        def index():
            return ''

        @fl.route('/image/put', methods=['PUT'])
        def put_image():
            log.info(
                'Saving image from {0}'.format(request.remote_addr))
            data = request.form.get('image', None)
            if data is None:
                return ('', 400)

            return jsonify({})

        @fl.route('/image/get/<ident>', methods=['GET'])
        def get_image(ident):
            return jsonify({})
