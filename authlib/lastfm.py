"""
Last.fm Authentication API

This is Version 1.0 of the Last.fm authentication API specification.

http://www.last.fm/ap/webauth
"""
import hashlib
import urlparse
import urllib

from . import interface

class Error(interface.Error):
    pass

class App(interface.Client):
    """
    """
    api_key = None
    secret = None

    def authenticate(self, session_token):
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
        return 'lastfm.App(%s)' % self.api_key


class Token(interface.User):
    key = None
    app = None
    user = None

    @property
    def auth(self):
        return Auth(self.app, self)


class Auth(interface.Auth):
    def __init__(self, app, sk=None, **kwargs):
        self.app = app
        self.sk = sk
        self.kwargs = kwargs

    def __call__(self, method, uri, body='', headers={}):
        """
        5. Make authenticated web service calls
        You can now sign your web service calls with a method signature,
        provided along with the session key you received in Section 4 and your
        API key. You will need to include all three as parameters in subsequent
        calls in order to be able to access services that require
        authentication. You can visit individual method call pages to find out
        if they require authentication. Your three authentication parameters
        are defined as:

            sk (Required) : The session key returned by auth.getSession service.
            api_key (Required) : Your 32-character API key.
            api_sig (Required) : Your API method signature, constructed as
                explained in Section 6
        """
        parts = urlparse.urlsplit(uri)
        query = dict(urlparse.parse_qsl(parts.query))
        query['api_key'] = self.app.key
        if self.sk:
            query['sk'] = self.sk
        if self.format == 'json':
            query['format'] = 'json'
        query.update(self.kwargs)
        query['api_sig'] = self.signature(query)
        uri = urlparse.urlunsplit((parts.scheme,
                                   parts.netloc,
                                   parts.path,
                                   urllib.urlencode(query),
                                   parts.fragment))
        return method, uri, body, headers

    def signature(self, **kwargs):
        """
        6. Sign your calls
        Construct your api method signatures by first ordering all the
        parameters sent in your call alphabetically by parameter name and
        concatenating them into one string using a <name><value> scheme. So for
        a call to auth.getSession you may have:

            api_keyxxxxxxxxmethodauth.getSessiontokenxxxxxxx

        Ensure your parameters are utf8 encoded. Now append your secret to
        this string. Finally, generate an md5 hash of the resulting string.
        For example, for an account with a secret equal to 'mysecret', your
        api signature will be:

            api signature = md5("api_keyxxxxxxxxmethodauth.getSessiontokenxxxxxxxmysecret")

        Where md5() is an md5 hashing operation and its argument is the
        string to be hashed. The hashing operation should return a
        32-character hexadecimal md5 hash.
        """
        param = ''.join(key+val for key, val in sorted(kwargs))
        param += self.app.secret
        param = param.encode('utf-8')
        return hashlib.md5().update(param).hexdigest()

