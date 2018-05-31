GIT LIST3R
##########

This tools compare websites against a git repo, then try to guess the last commit date.

Installation
============

To install the application:

.. code:: bash

    pip install git_list3r

Usage
=====

Example for a website named example.com:

.. code:: bash

	Usage:
	  git_list3r test [--timeout=<timeout>]
	                  [--web_base=<web_base>]
	                  [--file_base=<file_base>] <folder> <url>
	  git_list3r version <folder>
	  git_list3r -h | --help
	  git_list3r --version
