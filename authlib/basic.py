import base64
import callm

from . import interface

class Error(interface.Error):
    pass


def encode_pair(username, password):
    pair = '{}:{}'.format(username, password)
    enc_pair = base64.b64encode(pair)
    return 'Basic {}'.format(enc_pair)


def decode_pair(header):
    if not header[:6] == ('Basic '):
        raise Error('Non-Basic Authorization')
    enc_pair = header[6:]
    pair = base64.b64decode(enc_pair)
    return dict(zip(('username', 'password'), pair.split(':', 2)))


class Auth(interface.Auth):
    def __init__(self, consumer, token=None, **options):
        self.consumer = consumer
        self.token = token
        self.options = options

    def __call__(self, url, method, headers, body):
        """
        Return signed request parameters.
        """
        if self.token:
            headers['Authorization'] = encode_pair(
                    self.token.username, self.token.password)
        return url, method, headers, body


class Provider(callm.Connection):
    def get_redirect_url(self, callback_url):
        return callback_url


class ConsumerInterface(interface.Consumer):
    Auth = Auth
    Provider = Provider


class Consumer(ConsumerInterface):
    pass


class TokenInterface(interface.Token):
    consumer = Consumer()

    username = None
    password = None


class Token(TokenInterface):
    def __init__(self, username, password):
        self.username = username
        self.password = password

