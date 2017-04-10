import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='gradify',
    version='0.2',
    packages=find_packages(),
    license='MIT',
    description='A python library to generate CSS gradient from an image',
    long_description=README,
    url='https://github.com/QueraTeam/gradify',
    install_requires=[
        'Pillow>=4.1.0'
    ]
)
