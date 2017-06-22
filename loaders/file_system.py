from base_loader import BaseLoader
import os, sys
import Image 

class FileSystemLoader(BaseLoader):
	
	def __init__(self, arg):
		super(FileSystemLoader, self).__init__()

	def load_file(namespace, filename):
		
		image = Image.open(filename)

		return image

