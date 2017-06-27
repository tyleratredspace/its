#!/usr/bin/env python

from flask import Flask, request, abort
from pipeline import process_transforms
from loader import load_image

app = Flask(__name__)


# root
@app.route('/')
def index():
    return "Welcome to the Image Transformation service (ITS)"

# New ITS
# image transform command
@app.route('/<namespace>/<path:filename>', methods=['GET'])
def transform_image(namespace, filename):
    query = request.args

    image = load_image(namespace, filename)

    if image:
        abort(404)

    # transformation processor call
    return process_transforms(image, query)

# Old ITS Support
# @app.route('/<namespace>/<path:image>')
@app.route('/<namespace>/<path:image>.crop.<int:width>x<int:height>.<ext>')
def crop(namespace, image, width, height, ext):
	pass

@app.route('/<namespace>/<path:image>.fit.<int:width>x<int:height>.<ext>')
def fit(namespace, image, width, height, ext):
	pass

@app.route('/<namespace>/<path:image>.focalcrop.<int:width>x<int:height>.<int(min=0,max=100):x>.<int(min=0,max=100):y>.<ext>')
def focalcrop(namespace, image, width, height, x, y, ext):
	pass

@app.route('/<namespace>/<path:image>.resize.<int:width>x.passport.<ext>')
def resize_width_passport(namespace, image, width, ext):
	pass

@app.route('/<namespace>/<path:image>.resize.x<int:height>.passport.<ext>')
def resize_height_passport(namespace, image, height, ext):
	pass

@app.route('/<namespace>/<path:image>.resize.<int:width>x<int:height>.passport.<ext>')
def resize_passport(namespace, image, width, height, ext):
	pass

@app.route('/<namespace>/<path:image>.resize.<int:width>x.<ext>')
def resize_width(namespace, iamge, width, ext):
	pass

@app.route('/<namespace>/<path:image>.resize.x<int:height>..<ext>')
def resize_height(namespace, image, height, ext):
	pass

@app.route('/<namespace>/<path:image>.resize.<int:width>x<int:height>.<ext>')
def resize(namespace, image, width, height, ext):
	pass

if __name__ == '__main__':
    app.run(debug=True)
