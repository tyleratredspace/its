"""
Skeleton file for authentication handlers
"""


@auth.error_handler
def unauthorized():
    return "Missing permissions, please login in or change accounts"