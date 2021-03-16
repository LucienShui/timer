from __future__ import absolute_import, print_function

# read the contents of your README file
from os import path

from timer.__version__ import __name__, __version__, __author__, __author_email__, __url__, __description__

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    description=__description__,
    packages=['timer'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
