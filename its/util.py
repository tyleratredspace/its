from flask import request

from .errors import ITSInvalidImageFileError
from .settings import MIME_TYPES, NAMESPACES


def get_redirect_location(namespace, query, filename):
    config = NAMESPACES[namespace]
    redirect_url = "{url}?{query_param}={scheme}://{host}/{namespace}/{path}".format(
        url=config["url"],
        query_param=config["query-param"],
        scheme=request.scheme,
        host=request.host,
        namespace=namespace,
        path=filename,
    )
    ext = query.pop("format", None)
    for key, val in query.items():
        redirect_url = redirect_url + ".{key}.{val}".format(key=key, val=val)

    if ext:
        redirect_url = redirect_url + "." + ext

    return redirect_url


def validate_image_type(image):
    if image.format.upper() not in MIME_TYPES:
        raise ITSInvalidImageFileError("invalid image file")

    return image
