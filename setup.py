import os

from setuptools import setup

setup(
    name='pinvenv',
    version='0.1rc1',
    packages=['pin','pin.plugins'],
    namespace_packages=['pin', 'pin.plugins'],
    install_requires=['capn', 'virtualenv'],
    provides=['pinvenv'],
    author='Dustin Lacewell',
    author_email='dlacewell@gmail.com',
    url='https://github.com/dustinlacewell/pin-venv',
    description="VirtualEnv plugins for pin",
    long_description=open('README.markdown').read(),
)
