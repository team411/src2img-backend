from flask import Flask


class Router(Flask):

    def __init__(self, name, config):
        Flask.__init__(self, name)
        self.secret_key = config.get('flask', 'secret-key')
