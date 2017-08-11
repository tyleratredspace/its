
class BaseLoader(object):
    """
    Generic file loader class
    """
    slug = None
    parameter_name = None

    def __init__(self, arg):
        super(BaseLoader, self).__init__()
        self.arg = arg

    @staticmethod
    def load_image(namespace, filename, loader_slug):
        """
        Given a namespace (or directory name) and a filename, loads a file.
        """
        raise NotImplementedError

    @staticmethod
    def get_fileobj(namespace, filename):
        """
        Given a namespace (or directory name) and a filename,
        returns a file-like or bytes-like object.
        """
        raise NotImplementedError
