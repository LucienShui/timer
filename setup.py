from __future__ import absolute_import, print_function

# read the contents of your README file
from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='timer',
    version='0.0.3',
    author='Lucien Shui',
    author_email='lucien@lucien.ink',
    url='https://github.com/LucienShui/timer',
    description=u'Python Code Timer',
    packages=['timer'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
