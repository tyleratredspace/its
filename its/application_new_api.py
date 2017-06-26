#!/usr/bin/env python

from flask import Flask, request, abort
from pipeline import process_transforms
from loader import loader

app = Flask(__name__)


# root
@app.route('/')
def index():
    return "Welcome to the Image Transformation service (ITS)"


# image transform command
@app.route('/<namespace>/<path:filename>', methods=['GET'])
def transform_image(namespace, filename):
    query = request.args.to_dict()
    image = loader(namespace, filename)

    if image is None:
        abort(404)

    # transformation processor call
    return process_transforms(image, query)


if __name__ == '__main__':
    app.run(debug=True)
