#!/usr/bin/env python3

from io import BytesIO
from flask import Flask, request, abort, Response
from its.pipeline import process_transforms
from its.loader import loader

app = Flask(__name__)


def process_request(namespace, query, filename):
    image = loader(namespace, filename)
    image.info['filename'] = filename

    if image is None:
        abort(404)

    result = process_transforms(image, query)

    if result.format is None:
        result.format = image.format

    mime_type = "image/" + result.format.lower()

    output = BytesIO()
    result.save(output, format=result.format.upper())

    return Response(response=output.getvalue(), mimetype=mime_type)


def query_resize(width, height, ext):
    query = {'resize': 'x', 'format': str(ext)}

    if width is not None:
        query['resize'] = width + query['resize']

    if height is not None:
        query['resize'] = query['resize'] + height

    return query


# root
@app.route('/')
def index():
    return "Welcome to the Image Transformation service (ITS)"


# New ITS
# image transform command
@app.route('/<namespace>/<path:filename>', methods=['GET'])
def transform_image(namespace, filename):
    query = request.args.to_dict()
    result = process_request(namespace, query, filename)
    return result


# Old ITS Support
@app.route('/<namespace>/<path:filename>.crop.<width>x<height>.<ext>')
def crop(namespace, filename, width, height, ext):
    query = {'crop': width + 'x' + height, 'format': str(ext)}
    result = process_request(namespace, query, filename)
    return result


@app.route(
    '/<namespace>/<path:filename>.focalcrop.<width>x<height>.' +
    '<int(min=0,max=100):x>.<int(min=0,max=100):y>.<ext>')
def focalcrop(namespace, filename, width, height, x, y, ext):
    query = {'crop': width + 'x' + height + 'x' + x + 'x' + y, 'format': str(ext)}
    result = process_request(namespace, query, filename)
    return result


@app.route('/<namespace>/<path:filename>.fit.<width>x<height>.<ext>')
def fit(namespace, filename, width, height, ext):
    query = {'fit': width + 'x' + height, 'format': str(ext)}
    result = process_request(namespace, query, filename)
    return result


# resize with pseduo-optional arguments
@app.route('/<namespace>/<path:filename>.resize.<width>x<height>.<ext>')
@app.route('/<namespace>/<path:filename>.resize.x<height>.<ext>')
@app.route('/<namespace>/<path:filename>.resize.<width>x.<ext>')
def resize(namespace, filename, ext, width=None, height=None):
    query = query_resize(width, height, ext)
    result = process_request(namespace, query, filename)
    return result


# passport overlay resize with pseduo-optional arguments
@app.route('/<namespace>/<path:filename>.resize.<int:width>x<int:height>.passport.<ext>')
@app.route('/<namespace>/<path:filename>.resize.x<int:height>.passport.<ext>')
@app.route('/<namespace>/<path:filename>.resize.<int:width>x.passport.<ext>')
def resize_passport(namespace, filename, width, height, ext):
    query = query_resize(width, height, ext)
    query['overlay'] = 'passport'
    result = process_request(namespace, query, filename)
    return result


if __name__ == '__main__':
    app.run(debug=True)
