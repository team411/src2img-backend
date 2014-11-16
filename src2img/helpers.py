import os
import hashlib


class Helpers(object):

    @staticmethod
    def random_token(size=128):
        return hashlib.sha1(os.urandom(size)).hexdigest()
