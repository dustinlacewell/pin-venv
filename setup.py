import os

from distutils.core import setup

setup(
    name='pinvenv',
    version='0.1.2',
    packages=['pin.plugins'],
    install_requires=['pin', 'capn', 'virtualenv'],
    provides=['pinvenv'],
    author='Dustin Lacewell',
    author_email='dlacewell@gmail.com',
    url='https://github.com/dustinlacewell/pin-venv',
    description="VirtualEnv plugins for pin",
    long_description=open('README.markdown').read(),
)
