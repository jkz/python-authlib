from .. import interface

from .auth import Auth

class Connector(interface.Connector):
    def __init__(self, user=None):
        self.user = user

    @property
    def auth(self):
        return Auth(self.user)

