from .. import interface

from .auth import Auth

class Connector(interface.Connector):
    def __init__(self, client, token=None, **params):
        self.client = client
        self.token = token
        self.params = params

    @property
    def auth(self):
        return Auth(self.token, **self.params)
