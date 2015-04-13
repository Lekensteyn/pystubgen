#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'pystubgen',
    version = '0.1',
    description = 'Generates Python source code from a module for documentation purposes',
    #packages = find_packages(),
    py_modules = ['pystubgen'],

    # metadata for upload to PyPI
    author = 'Peter Wu',
    author_email = 'peter@lekensteyn.nl',
    license = 'MIT',
    keywords = 'development documentation',
    url = 'https://github.com/Lekensteyn/pystubgen',

    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Documentation',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        #'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    package_data = {
        '': ['README.md', 'LICENSE'],
    },

    entry_points={
        'console_scripts': [
            'pystubgen=pystubgen:main',
        ],
    },
)
