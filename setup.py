#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="its",
    version="2.0.0",
    py_modules=["its"],
    author="",
    author_email="",
    license="MIT",
    url="",
    long_description="",
    packages=find_packages(),
    description="image transformation service",
    platforms=["any"],
    install_requires=["flask", "pillow"],
    extras_require={"dev": ["flake8", "pytest"]},
)
