#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from rr.config.config_loader import ConfigLoader
from rr.config.app_validator import AppValidator
from rr.config.yaml_format import YamlFormat


class AppConfigLoader:
    def __init__(self):
        self._loader = ConfigLoader(YamlFormat(), AppValidator())

    def load(self, path):
        return self._loader.load(path)
