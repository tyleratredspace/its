class ITSError(Exception):
    """
    Base error class for ITS.
    """

    status_code = 400
    message = ""

    def __init__(self, error, status_code=None, payload=None, *args):

        self.message = self.message + error

        if status_code is not None:
            self.status_code = status_code

        self.payload = payload or dict()

        if args:
            self.args = args


class ConfigError(ITSError):
    """
    Class for errors that deal with ITS settings.
    """

    status_code = 500
    message = "Configuration Error: "


class ITSLoaderError(ITSError):
    """
    General class for errors that occur in the ITS loader.
    """

    status_code = 400
    message = "ITSLoaderError: "


class ITSTransformError(ITSError):
    """
    General class for errors occuring while applying transforms.
    """

    status_code = 400
    message = "ITSTransformError: "


class NotFoundError(ITSError):
    """
    General class for existance errors.
    """

    status_code = 404
    message = "NotFoundError: "
