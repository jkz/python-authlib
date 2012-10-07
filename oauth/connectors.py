from .. import interface

from .auth import Auth

class Connector(interface.Connector):
    def __init__(self, consumer, token=None, **params):
        self.consumer = consumer
        self.token = token
        self.params = params

    @property
    def auth(self):
        return Auth(self.consumer, self.token, **self.params)
