class Error(Exception):
    pass


class Auth(object):
    """
    Authorizes requests under satisfactory conditions.
    """
    def __call__(self, url, method, headers, body):
        """
        Return signed request paramters.
        """
        return url, method, headers, body


class Token(object):
    """
    Represents a user authorization for an app.
    """
    user = None
    app = None


class App(object):
    """
    Represents an authenticating entity.
    """
    def authenticate(self, **creds):
        """
        -> uid
        """
        return NotImplementedError

