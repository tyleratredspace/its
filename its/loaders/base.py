
class BaseLoader(object):
    """
    Generic file loader class
    """
    loader_slug = None

    def __init__(self, arg):
        super(BaseLoader, self).__init__()
        self.arg = arg

    def load_image(namespace, filename):
        """
        Given a namespace (or directory name) and a filename, loads a file.
        """
        raise NotImplementedError

    def get_fileobj(namespace, filename):
        """
        Given a namespace (or directory name) and a filename,
        returns a file-like or bytes-like object.
        """
        raise NotImplementedError
