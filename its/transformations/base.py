class BaseTransform(object):

    """
    Generic image transform type class
    """

    slug = None  # unique string that identifies a given transform

    def __init__(self, arg):
        super(BaseTransform, self).__init__()
        self.arg = arg

    def apply_transform(img, *args):

        raise NotImplementedError
