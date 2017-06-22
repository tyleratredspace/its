#!/usr/bin/env python

from flask import Flask, make_response, request, abort
from pipeline import process_transforms
from loader import load_image

app = Flask(__name__)

@app.route('/')  # root
def index():
	return "Welcome to the Image Transformation service (ITS)"


@app.route('/<namespace>/<path:filename>',methods=['GET']) #image transform command
def transform_image(namespace,filename):
	query = request.args

	image = load_image(namespace, filename)

	if not image:
		abort(404)

	return process_transforms(image,query) # transformation processor call

if __name__ == '__main__':
	app.run(debug=True)