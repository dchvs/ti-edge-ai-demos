#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>


from rr.config.app_validator import AppValidator
from rr.config.yaml_format import YamlFormat


class ConfigLoader:
    """
    Class that loads and verifies the app configuration file

    Attributes
    ----------
    _format : YamlFormat
        A private YamlFormat object
    _format : AppValidator
        A private AppValidator object

    Methods
    -------
    load(path : str)
        Parses and validates the configuration from the app configuration file
    """

    def __init__(self, appformat, validator):
        """
        Constructor for the Config Laoder object
        """

        self._format = appformat
        self._validator = validator

    def load(self, path):
        """Calls parse and validate methods from YamlFormat and AppValidator and returns a dictionary with the app configuration

        Parameters
        ----------
        path : str
            The path to the configuration file
        """

        cfg_obj = self._format.parse(path)
        self._validator.validate(cfg_obj)

        return cfg_obj
