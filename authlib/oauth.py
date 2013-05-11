import time
import random
import hmac
import hashlib
import base64
import urlparse
import urllib

import callm

from . import interface

class Error(interface.Error):
    pass

def _utf8_str(s):
    """Convert unicode to utf-8."""
    if isinstance(s, unicode):
        return s.encode("utf-8")
    else:
        return str(s)

def percent_encode(s):
    return urllib.quote(_utf8_str(s), '~')

def percent_encode_dict(d):
    return dict(map(percent_encode, tup) for tup in d.iteritems())

def normalize_url(url):
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)

    # Exclude default port numbers.
    if scheme == 'http' and netloc[-3:] == ':80':
        netloc = netloc[:-3]
    elif scheme == 'https' and netloc[-4:] == ':443':
        netloc = netloc[:-4]
    if scheme not in ('http', 'https'):
        raise ValueError("Unsupported URL %s (%s)." % (url, scheme))

    # Normalized URL excludes params, query, and fragment.
    return urlparse.urlunparse((scheme, netloc, path, None, None, None))

def build_base_string(method, url, parameter_string):
    # Prepare url by stripping fragments and query string
    base_url = normalize_url(url)
    return '&'.join((
            method.upper(),
            percent_encode(base_url),
            percent_encode(parameter_string)))

def build_header(header):
    return 'OAuth ' + ', '.join(('='.join
        ((percent_encode(k), '"%s"' % percent_encode(v)))
        for k, v in sorted(header.iteritems())))

class Auth(interface.Auth):
    """
    An OAuth authorizer.
    """
    def set_token(self, oauth_token, oauth_token_secret):
        class DummyToken:
            key = oauth_token
            secret = oauth_token_secret
        self.token = DummyToken

    def set_verifier(self, verifier):
        self.options['oauth_verifier'] = verifier

    @property
    def signing_key(self):
        #TODO: sometime do this without +
        key = percent_encode(self.consumer.secret) + '&'
        if self.token:
            key += percent_encode(self.token.secret)
        return key

    def signature(self, msg):
        """Builds a hmac_sha1 hash for the message."""
        key = self.signing_key.encode('ascii')
        raw = msg.encode('ascii')
        mac = hmac.new(key, raw, hashlib.sha1)
        dig = mac.digest()
        sig = base64.b64encode(dig)
        return sig

    def header(self, method, uri, **other_params):
        header = {}

        # Add the basic oauth paramters
        header['oauth_consumer_key'] = self.consumer.key
        header['oauth_signature_method'] = 'HMAC-SHA1'
        header['oauth_version'] = '1.0'
        header['oauth_timestamp'] = int(time.time())
        header['oauth_nonce'] = random.getrandbits(64)

        # Add token if we're authorizing a user
        if self.token:
            header['oauth_token'] = self.token.key

        # Override default header and add additional header params
        header.update(self.options)

        #XXX: Sorting should be done prior to encoding!
        #XXX: Is that so?

        # Prepare the parameter string for the base string
        params_dict = header.copy()
        params_dict.update(other_params)
        params_string = urllib.urlencode(sorted(params_dict.iteritems()))

        # Build the base string from prepared parameter string
        base_string = build_base_string(method, uri, params_string)

        # Build the signature and add it to the parameters
        signature = self.signature(base_string)
        header['oauth_signature'] = signature

        # Return the constructed authorization header
        return build_header(header)

    def __call__(self, method, uri, body=None, headers={}):
        """
        Encode and sign a request according to OAuth 1.0 spec.

        Heads up!

        Does not support duplicate keys.
        """
        # Split the uri for the query string parameters
        parts = urlparse.urlsplit(uri)
        query_params = urlparse.parse_qsl(parts.query)
        body_params = urlparse.parse_qsl(body or '')

        other_params = {}
        other_params.update(dict(query_params))
        other_params.update(dict(body_params))

        headers['Authorization'] = self.header(method, uri, **other_params)

        body = urllib.urlencode(body_params)
        uri = urlparse.urlunsplit((parts.scheme,
                                   parts.netloc,
                                   parts.path,
                                   urllib.urlencode(query_params),
                                   parts.fragment))

        return method, uri, body, headers


#TODO: detailed error messages
#TODO: GET or POST?
class Provider(callm.Connection):
    """
    Represents an authentication service.

    The constructor requires at least a `host` and an `auth` object
    """
    request_token_path = None
    access_token_path = None
    authorize_uri = None
    authenticate_uri = None

    def get_request_token(self):
        response = self.POST(self.request_token_path)
        if response.status != 200:
            raise Error('Invalid response while obtaining request token.')
        return response.query

    def get_access_token(self, key, secret, verifier):
        self.auth.set_token(key, secret)
        self.auth.set_verifier(verifier)
        response = self.POST(self.access_token_path)
        if response.status != 200:
            raise Error('Invalid response while obtaining access token.')
        return response.query

    # TODO: If one is missing, use the other
    def get_authenticate_url(self, **kwargs):
        return callm.URL(self.authenticate_uri, **kwargs)

    def get_authorize_url(self, **kwargs):
        return callm.URL(self.authorize_uri, **kwargs)


class ConsumerInterface(interface.Consumer):
    Auth = Auth
    Provider = Provider

    key = None
    secret = None


class Consumer(ConsumerInterface):
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret


class TokenInterface(interface.Token):
    key = None
    secret = None


class Token(TokenInterface):
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

