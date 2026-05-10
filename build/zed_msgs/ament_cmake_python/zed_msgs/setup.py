from setuptools import find_packages
from setuptools import setup

setup(
    name='zed_msgs',
    version='5.0.1',
    packages=find_packages(
        include=('zed_msgs', 'zed_msgs.*')),
)
