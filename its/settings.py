import os
import json

# Set DEBUG = True to enable debugging application.
DEBUG = os.environ.get('ITS_DEBUG', 'false').lower() == 'true'

MIME_TYPES = {
    'PNG': 'image/png',
    'JPEG': 'image/jpeg',
    'JPG': 'image/jpeg',
    'WEBP': 'image/webp',
    'SVG': 'image/svg+xml'
}

PNGQUANT_PATH = os.environ.get('ITS_PNGQUANT_PATH', "pngquant")

DEFAULT_JPEG_QUALITY = int(os.environ.get('ITS_DEFAULT_JPEG_QUALITY', "95"))

BACKENDS = json.JSONDecoder().decode(s=os.environ.get('ITS_BACKENDS', '{"default":{"loader":"http", "prefixes":[""]}}'))

OVERLAYS = json.JSONDecoder().decode(s=os.environ.get('ITS_OVERLAYS', '{"overlay":"None"}'))

OVERLAY_PLACEMENT = [
    int(os.environ.get('ITS_OVERLAY_PLACEMENT_X', '5')),
    int(os.environ.get('ITS_OVERLAY_PLACEMENT_Y', '5')) 
    ]

# the keyword used to recognize focal point args in filenames
FOCUS_KEYWORD = os.environ.get('ITS_FOCUS_KEYWORD', "focus-")

DELIMITERS_RE = os.environ.get('ITS_DELIMITERS_RE', "[x_,]")
