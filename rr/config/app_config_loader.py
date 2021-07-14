#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from rr.config.config_loader import ConfigLoader
from rr.config.app_validator import AppValidator
from rr.config.yaml_format import YamlFormat


class AppConfigLoader:
    """
    Class that serves as the App Config facade

    Attributes
    ----------
    _loader : ConfigLoader
        A private ConfigLoader object

    Methods
    -------
    load(path : str)
        Returns a dictionary with the app configuration
    """

    def __init__(self):
        """
        Constructor for the App Config Laoder object
        """

        self._loader = ConfigLoader(YamlFormat(), AppValidator())

    def load(self, path):
        """Returns the dictionary with the app configuration from the Config Loader object

        Parameters
        ----------
        path : str
            The path to the configuration file
        """

        return self._loader.load(path)
