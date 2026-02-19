from setuptools import find_packages
from setuptools import setup

setup(
    name='robotiq_85_msgs',
    version='1.0.1',
    packages=find_packages(
        include=('robotiq_85_msgs', 'robotiq_85_msgs.*')),
)
