class Error(Exception):
    pass


class Auth(object):
    """
    Authorizes requests under satisfactory conditions.
    """
    def __init__(self, app, token=None, **options):
        self.app = app
        self.token = token
        self.options = options

    def __call__(self, url, method, headers, body):
        """
        Return signed request paramters.
        """
        return url, method, headers, body


class App(object):
    """
    Represents an authenticating entity.
    """
    def authenticate(self, **creds):
        """
        -> uid
        """
        return NotImplementedError

    @property
    def auth(self):
        return self.Auth(self)

    @property
    def api(self):
        return self.API(auth=self.auth)

class Token(object):
    """
    Represents a user authorization for an app.
    """
    user = None
    app = None

    Auth = Auth
    API = API

    @property
    def auth(self):
        return self.app.Auth(self.app, self)

    @property
    def api(self):
        return self.app.API(auth=self.auth)


