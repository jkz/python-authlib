import base64

from . import interface

class Error(interface.Error):
    pass


class Auth(interface.Auth):
    pass


def encode_pair(username, password):
    pair = ':'.join((username, password))
    enc_pair = base64.b64encode(pair)
    return 'Basic %s' % enc_pair


def decode_pair(header):
    if not header[:6] == ('Basic '):
        raise Error('Non-Basic Authorization')
    enc_pair = header[6:]
    pair = base64.b64decode(enc_pair)
    return dict(zip(('username', 'password'), pair.split(':', 2)))

