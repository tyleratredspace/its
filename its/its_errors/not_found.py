from .its_error import ITSError


class NotFoundError(ITSError):
    """
    General class for existance errors.
    """

    status_code = 404
    message = "NotFoundError: "

    def __init__(self, message, status_code=None, payload=None, *args):

        self.message = self.message + message

        if status_code is not None:
            self.status_code = status_code

        self.payload = (payload or dict())

        if args:
            self.args = args
