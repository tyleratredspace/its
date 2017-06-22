
"""
Skeleton file for error handlerss
"""

@avail.error_handler
def resource_not_found():
	"""
		Return error if input image doesn't exist.
	"""
	return "Image not found in namespace"