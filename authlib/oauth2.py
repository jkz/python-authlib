import callm
import urlparse
import urllib

from . import interface

class Error(interface.Error):
    pass


class Auth(interface.Auth):
    """
    An OAuth 2 authenticator. Is associated with a client which can
    authenticate and register end users. If an enduser is associated with this
    authenticator, it can authorize requests.
    """
    def __call__(self, method, uri, body='', headers={}):
        """
        Add a token parameter tot the query string.

        Heads up!

        Does not support duplicate keys.
        """

        if self.token is not None:
            parts = urlparse.urlsplit(uri)
            query = dict(urlparse.parse_qsl(parts.query))
            query['client_id'] = self.token.key
            uri = urlparse.urlunsplit((parts.scheme,
                                       parts.netloc,
                                       parts.path,
                                       urllib.urlencode(query),
                                       parts.fragment))

        return method, uri, body, headers


class Provider(callm.Connection):
    exchange_code_url = None

    def request_code(self, redirect_uri, **kwargs):
        """Return a redirect url"""
        query = dict(client_id=self.auth.consumer.key, redirect_uri=redirect_uri)
        query.update(kwargs)
        return callm.URL(self.authenticate_uri, verbatim=False, **query)

    def exchange_code(self, code, redirect_uri, **kwargs):
        """
        Trade a code for access credentials. They are returned as a callm
        response object, to be decoded by the caller.
        """
        response = self.POST(
                self.exchange_code_url,
                code=code,
                redirect_uri=redirect_uri,
                client_id=self.auth.consumer.key,
                client_secret=self.auth.consumer.secret,
                **kwargs)

        if response.status != 200:
            #XXX: This is to show debug information
            status = response.status
            raw = response.raw
            print 'status:', status
            print 'raw', raw
            raise Error('Error occured while exchanging code')

        return response


class ConsumerInterface(interface.Consumer):
    Auth = Auth
    Provider = Provider

    key = None
    secret = None

    def provider(self):
        return self.Provider(auth=self.auth)

    def __str__(self):
        return 'oauth_consumer(%s)' % self.key

class Consumer(ConsumerInterface):
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret


class TokenInterface(interface.Token):
    consumer = None
    key = None
    expires = None

class Token(TokenInterface):
    def __init__(self, consumer, key):
        self.consumer = consumer
        self.key = key


