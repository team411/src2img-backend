import pykka
import logging
import json
import copy
from PyV8 import JSClass, JSContext, JSEngine, JSLocker

logging.basicConfig()
log = logging.getLogger('renderer')


class BemhtmlRenderer(pykka.ThreadingActor):

    def __init__(self, template):
        super(BemhtmlRenderer, self).__init__()
        with JSLocker():
            self.ctx = JSContext()
            with self.ctx as ctx:
                ctx.eval(template)

    def on_receive(self, message):
        with JSLocker():
            with self.ctx as ctx:
                bemjson = copy.copy(message['bemjson'])
                if 'mix' not in bemjson:
                    bemjson['mix'] = []

                bemjson['mix'].append({
                    'block': 'params',
                    'js': message.get('params', {})
                })

                res = ctx.eval(
                    'BEMHTML.apply({0})'.format(json.dumps(bemjson)))

            if message.get('gc', False):
                JSEngine.collect()

            return res

    def on_failure(*args):
        log.error(args)
