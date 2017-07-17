# import os

# Set DEBUG = True to enable debugging application.
DEBUG = True

IMAGE_LOADER = 's3'

OVERLAYS = {
	'passport': "static/Passport_Compass_Rose.png",
}

OVERLAY_PLACEMENT = [50, 50]

# the keyword used to recognize focal point args in filenames
FOCUS_KEYWORD = "focus-" 

DELIMITERS_RE = "[x_,]"