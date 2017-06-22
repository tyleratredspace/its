from its_loaders import *

def load_image(namespace, filename):

	""" 
		Cycles through the available loaders and attempts to load filename from namespace.
		if DEBUG=true, only uses FileSystemLoader
	"""
	loader_objs = base.BaseLoader.__subclasses__()
	print(loader_objs)
	# for obj in loader_objs:
	# 	print(obj)
		# image = obj.load_file(namespace,filename)

		# if image:
		# 	break

	# return 