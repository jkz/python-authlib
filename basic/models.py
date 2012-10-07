from .connectors import Connector

class Service(Connector):
    """
    Represents a connection with an authenticator.
    """
    authenticate_uri = None
    authorize_uri = None
