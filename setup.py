#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Eugenium',
    packages=['eugenium'],
    version='0.0.2',
    license='MIT',
    description=
    'Classes to create and deploy selenium processes on google cloud platform',
    author='Eugene Brown',
    author_email='efbbrown@gmail.com',
    url='https://github.com/efbbrown/eugenium',
    download_url="https://github.com/efbbrown/eugenium/archive/v_001.tar.gz",
    install_requires=[
        "selenium",
        "sqlalchemy"
    ])