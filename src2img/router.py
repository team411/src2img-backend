import flask


class Router(flask.Flask):

    def __init__(self, name, config):
        flask.Flask.__init__(self, name)
        self.secret_key = config.get('flask', 'secret-key')
