# -*- coding: utf-8 -*-
import os
import logging
from codecs import open
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from subprocess import check_call
import shlex

# Create post develop command class for hooking into the python setup process
# This command will run after dependencies are installed
class PostDevelopCommand(develop):
    def run(self):
        try:
            check_call(shlex.split("pre-commit install"))
        except Exception as e:
            logger.warning("Unable to run 'pre-commit install'")
        develop.run(self)


install_requires = ["networkx"]  # alternatively, read from `requirements.txt`
extra_requires = ["pandas"]  # optional dependencies
test_requires = ["pytest"]  # test dependencies
dev_requires = ["pre-commit"]  # dev dependencies

setup(
    name="packagename",
    version="v0.1.0",
    install_requires=install_requires,
    extras_require={"test": test_requires, "extra": extra_requires, "dev": test_requires + extra_requires + dev_requires,},
    cmdclass={"develop": PostDevelopCommand},
)
