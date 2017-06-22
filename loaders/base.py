
class BaseLoader(object):
	""" Generic file loader class """

	def __init__(self, arg):
		# super(BaseLoader, self).__init__()÷ß
		self.arg = arg
	
	def load_file(namespace, filename):
		""" Given a namespace (or directory name) and a filename, loads a file."""
		raise NotImplementedError