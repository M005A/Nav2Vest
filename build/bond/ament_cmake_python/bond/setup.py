from setuptools import find_packages
from setuptools import setup

setup(
    name='bond',
    version='4.2.0',
    packages=find_packages(
        include=('bond', 'bond.*')),
)
