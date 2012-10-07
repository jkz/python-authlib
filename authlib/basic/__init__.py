from callm import Url

from .. import interface

from .errors import Error
from . import utils

class Connector(interface.Connector):
    def __init__(self, client, user=None, **params):
        self.client = client
        self.user = user
        self.params = params

    @property
    def auth(self):
        return Auth(self.client, self.user, **self.params)


class Service(Connector):
    """
    Represents a connection with an authenticator.
    """
    authenticate_uri = None
    authorize_uri = None

    def get_redirect_url(self, **kwargs):
        return Url(self.authorize_uri, **kwargs)

class Auth(interface.Auth):
    """
    A Basic auth handler. If associated with a user, adds an authorization
    header to requests.
    """
    def __init__(self, client, user=None, **params):
        self.client = client
        self.user = user
        self.params = params

    def __call__(self, url, method, headers, body):
        """
        Add an encoded username/password pair header to request 
        """ 
        if self.user is not None:    
            headers['Authorization'] = utils.encode_pair(self.user.username,
                    self.user.password)

class Client(interface.Client):
    Service = Service

    def api(self, user=None, **params):
        return self.Service(self, user, **params)

    @property
    def service(self):
        return self.api()

    def authenticate(self, username, password):
        """
        -> uid
        """
        return NotImplementedError

class User(interface.User):
    username = None
    password = None

__all__ = ['Error', 'Connector', 'Auth', 'Service', 'Client', 'User']
