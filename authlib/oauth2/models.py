import callm

from .. import interface

from .errors import Error

from .connectors import Connector

class Service(Connector):
    exchange_code_url = None

    def request_code(self, redirect_uri, **kwargs):
        """Return a redirect url"""
        query = dict(client_id=self.client.id, redirect_uri=redirect_uri)
        query.update(kwargs)
        url = callm.Url(self.authenticate_uri, verbatim=False, **query)
        return url

    def exchange_code(self, code, redirect_uri, **kwargs):
        """
        Trade a code for an access credentials, then return the token after
        processing.
        """
        response = self.POST(
                self.exchange_code_url,
                code=code,
                redirect_uri=redirect_uri,
                client_id=self.client.id,
                client_secret=self.client.secret, 
                **kwargs)
            
        if response.status != 200:
            raise Error('Error occured while exchanging code')

        try:
            creds = response.query
        except ValueError:
            error = response.json
            raise Error(error['type'], error['message'])

        return self.client.process_creds(**creds)

class ClientInterface(interface.Client):
    id = None
    secret = None

    Service = Service

    def api(self, token=None, **params):
        return self.Service(self, token, **params)

    @property
    def service(self):
        return self.api()

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


class Token(interface.User):
    access_token = None
    expires =  None
