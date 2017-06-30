from .its_error import ITSError


class ConfigError(ITSError):
    """
    Class for errors that deal with ITS settings.
    """

    status_code = 500
    message = "Configuration Error: "

    def __init__(self, message, status_code=None, payload=None, *args):

        self.message = self.message + message

        if status_code is not None:
            self.status_code = status_code

        self.payload = (payload or dict())

        if args:
            self.args = args
