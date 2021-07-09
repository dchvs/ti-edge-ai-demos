#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import unittest

from rr.config.yaml_format import YamlFormat, YamlFormatError


class TestYamlFormat(unittest.TestCase):
    _path = 'tests/config/test_yaml.yaml'

    def test_sucess(self):
        formatter = YamlFormat()

        cfg = formatter.parse(self._path)

        self.assertEqual(10, cfg['test'])

    def test_file_not_found(self):
        non_existent = 'tests/config/test_yaml_nonexistent.yaml'

        formatter = YamlFormat()

        with self.assertRaises(YamlFormatError) as e:
            formatter.parse(non_existent)

        self.assertEqual("Unable to find configuration file", str(e.exception))

    def test_invalid(self):
        invalid = 'tests/config/test_yaml_invalid.yaml'

        formatter = YamlFormat()

        with self.assertRaises(YamlFormatError) as e:
            formatter.parse(invalid)

        self.assertEqual("Provided config file is invalid", str(e.exception))


if __name__ == '__main__':
    unittest.main()
