from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='git_list3r',
    version='1.0.0',
    description='Search for repo files on a website, and guess the last commit version',
    long_description=long_description,
    url='https://github.com/Antonin-Deniau/git_list3r',
    author='DENIAU Antonin',
    author_email='antonin.deniau@protonmail.com',
    license='GNU General Public License v3 or later (GPLv3+)',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='git enumeration framework',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['GitPython', 'requests', 'pathlib'],

    extras_require={},

    entry_points={
      'console_scripts': [
        'git_list3r=git_list3r.main:main',
      ],
    },
)
