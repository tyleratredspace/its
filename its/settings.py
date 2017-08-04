import os


# Set DEBUG = True to enable debugging application.
DEBUG = os.environ.get('ITS_DEBUG', 'false').lower() == 'true'

MIME_TYPES = {
    'PNG': os.environ.get('ITS_MIME_TYPE_PNG', 'image/png'),
    'JPEG': os.environ.get('ITS_MIME_TYPE_JPEG', 'image/jpeg'),
    'JPG': os.environ.get('ITS_MIME_TYPE_JPEG', 'image/jpeg'),
    'WEBP': os.environ.get('ITS_MIME_TYPE_WEBP', 'image/webp'),
    'SVG': os.environ.get('ITS_MIME_TYPE_WEBP', 'image/svg+xml')
}

PNGQUANT_PATH = os.environ.get('ITS_PNGQUANT_PATH', "pngquant")

DEFAULT_JPEG_QUALITY = int(os.environ.get('ITS_DEFAULT_JPEG_QUALITY', "95"))

IMAGE_LOADER = os.environ.get('ITS_IMAGE_LOADER', 's3')

OVERLAY_LOADER = os.environ.get('ITS_OVERLAY_LOADER', 's3')

BUCKETS = {
	'default': 'default',
	'kids': 'kids',
	'front_end': 'front_end',
	'ga': 'ga',
	'apps': 'apps'
}

OVERLAYS = {
    'overlay': "/static/overlay.png",
}

OVERLAY_PLACEMENT = [
    int(os.environ.get('ITS_OVERLAY_PLACEMENT_X', '5')),
    int(os.environ.get('ITS_OVERLAY_PLACEMENT_Y', '5')) 
    ]

# the keyword used to recognize focal point args in filenames
FOCUS_KEYWORD = os.environ.get('ITS_FOCUS_KEYWORD', "focus-")

DELIMITERS_RE = os.environ.get('ITS_DELIMITERS_RE', '[x_,]')
