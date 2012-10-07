import callm

#TODO: Server

class Error(Exception):
    pass


class Auth(object):
    """
    Authorizes requests under satisfied conditions.
    """
    def __call__(self, url, method, headers, body):
        #XXX: This needs a good look, prolly pass headers and query for inplace
        #     modification.
        """
        Perform actions and edit query/headers in place for authorization.
        """ 
        pass


class Connector(callm.Connector):
    """
    Represents a connection with an authenticator.
    """
    @property
    def auth(self):
        """
        -> Auth
        """
        raise NotImplementedError


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

