from .. import interface

from .auth import Auth
from .api import API

class App(interface.App):
    id = None
    secret = None

    Auth = Auth
    API = API

    def authenticate(self, access_token):
        """
        -> uid
        """
        raise NotImplementedError

    def process_creds(**creds):
        """
        -> access_token
        """
        raise NotImplementedError

    def __unicode__(self):
        return 'oauth.Client(%s)' % self.key


class Token(interface.Token):
    access_token = None
    expires =  None

