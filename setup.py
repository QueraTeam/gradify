import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='gradify',
    version='0.3.3',
    description='A python library to generate CSS gradient from an image',
    long_description=README,
    url='https://github.com/QueraTeam/gradify',
    download_url='https://pypi.python.org/pypi/gradify',
    license='MIT',
    py_modules=['gradify'],
    install_requires=[
        'Pillow>=4.1.0'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
