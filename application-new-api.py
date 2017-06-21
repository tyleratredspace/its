#!ENV/bin/python

from flask import Flask,make_response,request
from its_hub import process_transforms

app = Flask(__name__)

@app.route('/') #root
def index():
	return "Welcome to the Image Transformation service (ITS)"

@app.route('/<namespace>/',methods=['POST']) #namespace root, create image
def create_in_namespace(namespace):
	return "Creating new image in namespace"

@app.route('/<namespace>/',methods=['DELETE']) #namespace root, delete image
def delete_in_namespace(namespace):
	return "delete image in namespace"

@app.route('/<namespace>/<path:image>',methods=['POST']) #image input without transformations specified
	def transformless(namespace, image):

		transforms_dict = dict()  # keys are transform name, values are lists of arguments

		# parse request into transforms_dict
		# process_transforms(image,transforms_dict) # transformation processor call 
		
		# return "This should return the image as is or return it as a WebP"

@app.route('/<namespace>/<path:image>?<transforms_string>',methods=['POST']) #image transform command
	def transform_image():

		transforms_dict = dict()
		# parse request into transforms_dict
		# parse_request(transforms_string)

		# process_transforms(image,transforms_dict) # transformation processor call 

def parse_request(transforms_string):
	"""
		Takes in a string of transformation commands and outputs a dict
	"""
	request_dict = dict()

	return request_dict

if __name__ == '__main__':
	app.run(debug=True)