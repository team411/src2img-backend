from .singleton import Singleton
import os
import logging
import pykka
from .config_loader import ConfigLoader
from .config_parser import ConfigParser
from .router import Router
from .routes import Routes

__file_dir__ = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(__file_dir__, 'VERSION'), 'r') as fd:
    VERSION = fd.read()

DEV_ENV = 'development'
PROD_ENV = 'production'

DEFAULT_LOG_LEVEL = 'INFO'
DEFAULT_ENV = DEV_ENV

ENV = os.environ.get('ENV', DEFAULT_ENV)

CONFIG_NAME = 'app.ini'

if ENV == DEV_ENV:
    CONFIG_PATHS = [
        '{0}/config/{1}'.format(os.getcwd(), env)
        for env in ['base', ENV]
    ]
else:
    CONFIG_PATHS = ['/etc/src2img']


class App(object):
    __metaclass__ = Singleton
    __version__ = VERSION

    def __init__(self):
        self._ready = False

    def setup(self):
        if self._ready:
            return
        logging.basicConfig()
        self.log = logging.getLogger('src2img')
        self.log.setLevel(
            getattr(logging, os.environ.get('LOG_LEVEL', DEFAULT_LOG_LEVEL).upper()))
        self.config = ConfigLoader(CONFIG_PATHS, CONFIG_NAME)
        self.router = Router('src2img', self.config)
        self._routes = Routes(self.router, self)
        self._routes.setup()
        self._ready = True

    def run(self):
        if not self._ready:
            raise RuntimeError('You need to call setup() first')
        host = self.config.get('flask', 'host')
        port = int(self.config.get('flask', 'port'))
        self.log.info('Listening on {0}:{1}'.format(host, port))
        self.router.run(
            host=host,
            port=port,
            debug=bool(self.config.get('flask', 'debug')),
            threaded=True
        )

    def teardown(self):
        self.log.info('Teardown')
        pykka.ActorRegistry.stop_all()
