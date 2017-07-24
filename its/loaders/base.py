
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
