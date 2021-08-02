#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>
#
#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

import os
import logging
from codecs import open
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from subprocess import check_call
import shlex
import unittest

# Create post develop command class for hooking into the python setup process
# This command will run after dependencies are installed

name = 'ti-edge-ai-demos'
version = '0.1.0'
author = 'RidgeRun'

tested = False


class PostDevelopCommand(develop):
    def run(self):
        try:
            check_call(shlex.split("pre-commit install"))
        except Exception as e:
            logger.warning("Unable to run 'pre-commit install'")
        develop.run(self)


# alternatively, read from `requirements.txt`
install_requires = ["setuptools", "wheel"]
extra_requires = []  # optional dependencies
test_requires = ["unittest"]  # test dependencies
dev_requires = ["pre-commit"]  # dev dependencies

setup(
    name=name,
    version=version,
    description='RidgeRun Edge AI Demos',
    long_description='RidgeRun custom demos from TI Computer Vision and Deep Learning SDKs',
    long_description_content_type='text/markdown',
    author=author,
    author_email='support@ridgerun.com',

    packages=find_packages(
        exclude=[
            "*.tests",
            "*.tests.*",
            "tests.*",
            "tests"]),
    scripts=[
        'main.py',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3',
    install_requires=install_requires,
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
            'source_dir': ('setup.py', 'doc')}},

    extras_require={
        "test": test_requires,
        "extra": extra_requires,
        "dev": test_requires + extra_requires + dev_requires,
    },
    cmdclass={"develop": PostDevelopCommand},
)
