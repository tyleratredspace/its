from .its_error import ITSError


class ITSLoaderError(ITSError):
    """
    General class for errors that occur in the ITS loader.
    """

    status_code = 400
    message = "ITSLoaderError: "

    def __init__(self, message, status_code=None, payload=None, *args):

        self.message = self.message + message

        if status_code is not None:
            self.status_code = status_code

        self.payload = (payload or dict())

        if args:
            self.args = args
