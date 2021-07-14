#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import unittest

from rr.config.app_validator import AppValidator
from rr.config.config_loader import ConfigLoader
from rr.config.yaml_format import YamlFormat


class TestYamlFormat(unittest.TestCase):

    def setUp(self):
        self.path = "tests/config/test_config.yaml"
        self.output_cfg = {
            'streams': [{'id': 'stream0',
                         'uri': 'http0',
                         'triggers': ['person_recording',
                                      'person_logging']},
                        {'id': 'stream1',
                         'uri': 'http1',
                         'triggers': ['person_recording',
                                      'animal_logging']}],
            'filters': [{'name': 'person_filter',
                         'labels': ['male',
                                    'child'],
                         'threshold': 0.7},
                        {'name': 'animal_filter',
                            'labels': ['cat',
                                       'dog'],
                            'threshold': 0.8}],
            'actions': [{'name': 'start_recording',
                         'type': 'recording',
                         'lenght': 10,
                         'location': '/tmp/recording%d.mp4'},
                        {'name': 'log_event',
                            'type': 'logging',
                            'location': '/tmp/log.xls'}],
            'triggers': [{'name': 'person_recording',
                          'action': 'start_recording',
                          'filters': ['person_filter',
                                      'animal_filter']},
                         {'name': 'person_logging',
                             'action': 'log_event',
                             'filters': ['person_filter']},
                         {'name': 'animal_logging',
                             'action': 'log_event',
                             'filters': ['animal_filter']}]}

    def test_config_loader(self):
        cfg = ConfigLoader(YamlFormat(), AppValidator())
        cfg_obj = cfg.load(self.path)

        self.assertEqual(self.output_cfg, cfg_obj)


if __name__ == '__main__':
    unittest.main()
