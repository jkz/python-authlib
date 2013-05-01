class Error(Exception):
    pass


class Auth(object):
    """
    Authorizes requests under satisfactory conditions.
    """
    def __init__(self, consumer, token=None, **options):
        self.consumer = consumer
        self.token = token
        self.options = options

    def __call__(self, url, method, headers, body):
        """
        Return signed request parameters.
        """
        return url, method, headers, body


class Consumer(object):
    """
    Represents an authenticating entity.
    """
    # A class that authorizes requests by signing their parameters
    Auth = Auth

    # A class that provides the authentication service
    Provider = NotImplemented

    # A class that executes authenticated calls
    API = NotImplemented


    def auth_process(self, **creds):
        """
        -> uid
        """
        return NotImplementedError

    @property
    def auth(self):
        return self.Auth(self)

    @property
    def provider(self):
        return self.Provider(auth=self.auth)

    @property
    def api(self):
        return self.API(auth=self.auth)


class Token(object):
    """
    Represents a user authorization for a consumer
    """
    consumer = Consumer()

    @property
    def auth(self):
        return self.consumer.Auth(self.consumer, self)

    @property
    def api(self):
        return self.consumer.API(auth=self.auth)


