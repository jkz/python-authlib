class Error(Exception):
    pass


class Auth(object):
    """
    Authorizes requests under satisfied conditions.
    """
    def __call__(self, url, method, headers, body):
        """
        Return signed request paramters.
        """
        return url, method, headers, body


class User(object):
    """
    Represents a user with a uid.
    """
    pass


class Client(object):
    """
    Represents an authenticating entity.
    """
    def authenticate(self, **creds):
        """
        -> uid
        """
        return NotImplementedError

