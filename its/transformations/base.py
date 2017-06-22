
class BaseTransform(object):

    """
    Generic image transform type class
    """

    def __init__(self, arg):
        super(BaseTransform, self).__init__()
        self.arg = arg

    def apply_transformation(img, *args):

        pass

        # if(len(transformation_list) == 0):
        # 	return img
