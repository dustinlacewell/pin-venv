import os

from distutils.core import setup

setup(
    name='pin-venv',
    version='0.5',
    packages=['pin.plugins'],
    requires=['pin', 'capn', 'virtualenv'],
    author='Dustin Lacewell',
    author_email='dlacewell@gmail.com',
    url='https://github.com/dustinlacewell/pin-venv',
    description="VirtualEnv plugins for pin",
    long_description=open('README.markdown').read(),
)
