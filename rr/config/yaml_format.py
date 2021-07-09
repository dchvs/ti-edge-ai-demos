#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import yaml


class YamlFormatError(RuntimeError):
    pass


class YamlFormat:
    def parse(self, path):

        try:
            with open(path, 'r') as stream:
                cfg = yaml.safe_load(stream)
        except FileNotFoundError as e:
            raise YamlFormatError("Unable to find configuration file") from e
        except yaml.parser.ParserError as e:
            raise YamlFormatError("Provided config file is invalid") from e

        return cfg
