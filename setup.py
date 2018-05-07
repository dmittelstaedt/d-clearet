#!/usr/bin/env python
# TODO: Write setup file

from distutils.core import setup

setup(
    name='clearet',
    version='0.0.1',
    description='Removing outdated files based on their extenstion',
    author='David Mittelstaedt',
    author_email='david.mittelstaedt@dataport.de',
    url='https://github.com/dmittelstaedt/d-clearet',
    packages=['clearet', 'test'],
    data_files=[
        ('clearet/conf', ['clearet/conf/clearet.ini']),
        ('clearet/log', []),
        ('bin', ['bin/clearet'])]
    )
