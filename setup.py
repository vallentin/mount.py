#!/usr/bin/env python

# Author: Christian Vallentin <mail@vallentinsource.com>
# Website: http://vallentinsource.com
# Repository: https://github.com/MrVallentin/mount.py
#
# Date Created: March 27, 2016
# Last Modified: March 27, 2016
#
# Developed and tested using Python 3.5.1

from distutils.core import setup

import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

setup(
	name="mount.py",
	version="1.0",
	py_modules=["mount"],
	author="Christian Vallentin",
	author_email="mail@vallentinsource.com",
	url="https://github.com/MrVallentin/mount.py",
	description="Python only module for listing, mounting and unmounting media devices",
	long_description="mount.py is a simple, small and self-contained Python only module, for listing, mounting and unmounting media drives on Linux.",
	keywords="listing media devices mount mounting unmount unmounting",
	license="MIT",
	classifiers=[
		"Development Status :: 1 - Alpha",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Operating System :: UNIX",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
	]
)
