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
    query = request.args.to_dict()
    query['filename'] = filename

    image = load_image(namespace, filename)

    if image is None:
        abort(404)

    # transformation processor call
    return process_transforms(image, query)

# Old ITS Support
@app.route('/<namespace>/<path:filename>.crop.<int:width>x<int:height>.<ext>')
def crop(namespace, image, width, height, ext):
    query = {'crop':width + 'x' + height,'format':str(ext)}
    query['filename'] = filename

    image = load_image(namespace, image)

    if image is None:
        abort(404)

    # transformation processor call
    return process_transforms(image, query)

@app.route('/<namespace>/<path:filename>.fit.<int:width>x<int:height>.<ext>')
def fit(namespace, image, width, height, ext):
	query = {'fit':width + 'x' + height,'format':str(ext)}
    query['filename'] = filename

    image = load_image(namespace, image)

    if image is None:
        abort(404)

    # transformation processor call
    return process_transforms(image, query)

@app.route('/<namespace>/<path:image>.focalcrop.<int:width>x<int:height>.<int(min=0,max=100):x>.<int(min=0,max=100):y>.<ext>')
def focalcrop(namespace, image, width, height, x, y, ext):
    query = {'crop':width + 'x' + height + 'x' + x + 'x' + y,'format':str(ext)}
    query['filename'] = filename

    image = load_image(namespace, image)

    if image is None:
        abort(404)

    # transformation processor call
    return process_transforms(image, query)

@app.route('/<namespace>/<path:image>.resize.<int:width>x.passport.<ext>')
def resize_width_passport(namespace, image, width, ext):
    query = {'resize':width + 'x','overlay':'passport','format':str(ext)}
    query['filename'] = filename

    image = load_image(namespace, image)

    if image is None:
        abort(404)

    # transformation processor call
    return process_transforms(image, query)

@app.route('/<namespace>/<path:image>.resize.x<int:height>.passport.<ext>')
def resize_height_passport(namespace, image, height, ext):
    query = {'resize':'x'+ height,'overlay':'passport','format':str(ext)}
    query['filename'] = filename

    image = load_image(namespace, image)

    if image is None:
        abort(404)

    # transformation processor call
    return process_transforms(image, query)

@app.route('/<namespace>/<path:image>.resize.<int:width>x<int:height>.passport.<ext>')
def resize_passport(namespace, image, width, height, ext):
    query = {'resize':width + 'x'+ height,'overlay':'passport','format':str(ext)}
    query['filename'] = filename

    image = load_image(namespace, image)

    if image is None:
        abort(404)

    # transformation processor call
    return process_transforms(image, query)

@app.route('/<namespace>/<path:image>.resize.<int:width>x.<ext>')
def resize_width(namespace, iamge, width, ext):
	query = {'resize':width + 'x','format':str(ext)}
    query['filename'] = filename

    image = load_image(namespace, image)

    if image is None:
        abort(404)

    # transformation processor call
    return process_transforms(image, query)

@app.route('/<namespace>/<path:image>.resize.x<int:height>.<ext>')
def resize_height(namespace, image, height, ext):
	query = {'resize':'x' + height,'format':str(ext)}
    query['filename'] = filename

    image = load_image(namespace, image)

    if image is None:
        abort(404)

    # transformation processor call
    return process_transforms(image, query)

@app.route('/<namespace>/<path:image>.resize.<int:width>x<int:height>.<ext>')
def resize(namespace, image, width, height, ext):
	query = {'resize':width + 'x'+ height,'format':str(ext)}
    query['filename'] = filename

    image = load_image(namespace, image)

    if image is None:
        abort(404)

    # transformation processor call
    return process_transforms(image, query)

if __name__ == '__main__':
app.run(debug=True)
