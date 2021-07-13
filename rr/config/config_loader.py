#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>


from rr.config.app_validator import AppValidator
from rr.config.yaml_format import YamlFormat


class ConfigLoader:
    def __init__(self, appformat, validator):
        self._format = appformat
        self._validator = validator

    def load(self, path):
        cfg_obj = self._format.parse(path)
        self._validator.validate(cfg_obj)

        return cfg_obj


class AppConfigLoader:
    def __init__(self):
        self._loader = ConfigLoader(YamlFormat(), AppValidator())

    def load(self, path):
        return self._loader.load(path)
