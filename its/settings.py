

# Set DEBUG = True to enable debugging application.
DEBUG = True

MIME_TYPES = {
    'PNG': 'image/png',
    'JPEG': 'image/jpeg',
    'JPG': 'image/jpeg',
    'WEBP': 'image/webp',
    'SVG': 'image/svg+xml'
}

PNGQUANT_PATH = "pngquant"

PNGQUANT_DEFAULT_SPEED = '10'

PNGQUANT_DEFAULT_MAX_QUALITY = '100'

DEFAULT_JPEG_QUALITY = 95

IMAGE_LOADER = 'file_system'

OVERLAYS = {
    'passport': "static/Passport_Compass_Rose.png",
}

OVERLAY_PLACEMENT = [50, 50]

# the keyword used to recognize focal point args in filenames
FOCUS_KEYWORD = "focus-"

DELIMITERS_RE = "[x_,]"
