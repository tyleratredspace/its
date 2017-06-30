

class ITSError(Exception):
    """
    Base error class for ITS.
    """

    status_code = 400

    def __init__(self, message, status_code=None, payload=None, *args):

        self.message = message

        if status_code is not None:
            self.status_code = status_code

        self.payload = (payload or dict())

        if args:
            self.args = args
