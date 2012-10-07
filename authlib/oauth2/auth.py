import urlparse
import urllib

from .. import interface

class Auth(interface.Auth):
    """
    An OAuth 2 authenticator. Is associated with a client which can
    authenticate and register end users. If an enduser is associated with this
    authenticator, it can authorize requests. 
    """
    def __init__(self, token=None):
        self.token = token
        
    def __call__(self, method, uri, body='', headers={}):
        """
        Add a token parameter tot the query string. 

        Heads up!

        Does not support duplicate keys.
        """ 
        if self.token is not None:
            parts = urlparse.urlsplit(uri)
            query = dict(urlparse.parse_qsl(parts.query))
            query['access_token'] = self.token.access_token
            uri = urlparse.urlunsplit((parts.scheme,
                                       parts.netloc,
                                       parts.path,
                                       urllib.urlencode(query),
                                       parts.fragment))
        return method, uri, body, headers
            


