#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import unittest

from rr.config.app_validator import AppValidator, AppValidatortError, validate_streams, validate_filters, validate_actions, validate_triggers


class TestYamlFormat(unittest.TestCase):

    def test_streams(self):
        cfg_obj1 = {'streams': [
            {'id': 'stream0', 'uri': 'http0', 'triggers': ['person_recording']}]}
        cfg_obj2 = {'triggers': 'test', 'filters': 0}
        cfg_obj3 = {'streams': 'test'}

        triggers_list = ['person_recording']
        streams_validate = validate_streams(cfg_obj1, triggers_list)

        with self.assertRaises(AppValidatortError) as e1:
            validate_streams(cfg_obj2, triggers_list)

        with self.assertRaises(AppValidatortError) as e2:
            validate_streams(cfg_obj3, triggers_list)

        self.assertEqual(None, streams_validate)
        self.assertEqual("Streams field not found", str(e1.exception))
        self.assertEqual(
            "Found streams field, but is is not a list", str(
                e2.exception))

    def test_id_errors(self):
        cfg_obj1 = {'streams': [
            {'test': 'stream0', 'uri': 'http0', 'triggers': ['person_recording']}]}
        cfg_obj2 = {'streams': [
            {'id': 0, 'uri': 'http0', 'triggers': ['person_recording']}]}

        triggers_list = ['person_recording']

        with self.assertRaises(AppValidatortError) as e1:
            validate_streams(cfg_obj1, triggers_list)

        with self.assertRaises(AppValidatortError) as e2:
            validate_streams(cfg_obj2, triggers_list)

        self.assertEqual("Id field not found in stream", str(e1.exception))
        self.assertEqual(
            "Found id field in stream, but is is not a string", str(
                e2.exception))

    def test_uri_errors(self):
        cfg_obj1 = {'streams': [
            {'id': 'stream0', 'test': 'http0', 'triggers': ['person_recording']}]}
        cfg_obj2 = {'streams': [
            {'id': 'stream0', 'uri': 0, 'triggers': ['person_recording']}]}

        triggers_list = ['person_recording']

        with self.assertRaises(AppValidatortError) as e1:
            validate_streams(cfg_obj1, triggers_list)

        with self.assertRaises(AppValidatortError) as e2:
            validate_streams(cfg_obj2, triggers_list)

        self.assertEqual("Uri field not found in stream", str(e1.exception))
        self.assertEqual(
            "Found uri field in stream, but is is not a string", str(
                e2.exception))

    def test_streams_triggers_errors(self):
        cfg_obj1 = {'streams': [
            {'id': 'stream0', 'uri': 'http0', 'test': ['person_recording']}]}
        cfg_obj2 = {'streams': [
            {'id': 'stream0', 'uri': "http0", 'triggers': 'test'}]}
        cfg_obj3 = {'streams': [
            {'id': 'stream0', 'uri': 'http0', 'triggers': [0]}]}
        cfg_obj4 = {'streams': [
            {'id': 'stream0', 'uri': 'http0', 'triggers': ['person_recording', 'test']}]}

        triggers_list = ['person_recording']

        with self.assertRaises(AppValidatortError) as e1:
            validate_streams(cfg_obj1, triggers_list)
        with self.assertRaises(AppValidatortError) as e2:
            validate_streams(cfg_obj2, triggers_list)
        with self.assertRaises(AppValidatortError) as e3:
            validate_streams(cfg_obj3, triggers_list)
        with self.assertRaises(AppValidatortError) as e4:
            validate_streams(cfg_obj4, triggers_list)

        self.assertEqual(
            "Triggers field not found in stream", str(
                e1.exception))
        self.assertEqual(
            "Found triggers field in stream, but is is not a list", str(
                e2.exception))
        self.assertEqual(
            "Found trigger element in stream, but it is not a string", str(
                e3.exception))
        self.assertEqual("Stream has a not defined trigger", str(
            e4.exception))

    def test_filters(self):
        cfg_obj1 = {'filters': [{'name': 'person_filter',
                                 'labels': ['male', 'child'], 'threshold': 0.7}]}
        cfg_obj2 = {'streams': 'test1', 'triggers': 'test2'}
        cfg_obj3 = {'filters': 'test'}

        filters_list = ['person_filter']

        filters_validate = validate_filters(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e1:
            validate_filters(cfg_obj2)

        with self.assertRaises(AppValidatortError) as e2:
            validate_filters(cfg_obj3)

        self.assertEqual(filters_list, filters_validate)
        self.assertEqual("Filters field not found", str(e1.exception))
        self.assertEqual(
            "Found filters field, but is is not a list", str(
                e2.exception))

    def test_filters_name_errors(self):
        cfg_obj1 = {'filters': [
            {'labels': ['male', 'child'], 'threshold': 0.7}]}
        cfg_obj2 = {'filters': [
            {'name': [], 'labels': ['male', 'child'], 'threshold': 0.7}]}

        with self.assertRaises(AppValidatortError) as e1:
            validate_filters(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            validate_filters(cfg_obj2)

        self.assertEqual(
            "Name field not found in filter", str(
                e1.exception))
        self.assertEqual(
            "Found name field in filter, but it is not a string", str(
                e2.exception))

    def test_labels_errors(self):
        cfg_obj1 = {'filters': [{'name': 'recording',
                                 'test': ['male', 'child'], 'threshold': 0.7}]}
        cfg_obj2 = {'filters': [
            {'name': 'recording', 'labels': 'test', 'threshold': 0.7}]}
        cfg_obj3 = {'filters': [{'name': 'recording',
                                 'labels': [0, 'child'], 'threshold': 0.7}]}

        with self.assertRaises(AppValidatortError) as e1:
            validate_filters(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            validate_filters(cfg_obj2)

        with self.assertRaises(AppValidatortError) as e3:
            validate_filters(cfg_obj3)

        self.assertEqual(
            "Labels field not found in filter", str(
                e1.exception))
        self.assertEqual(
            "Found labels field in filter, but it is not a list", str(
                e2.exception))
        self.assertEqual(
            "Found label element in filter, but it is not a string", str(
                e3.exception))

    def test_threshold_errors(self):
        cfg_obj1 = {'filters': [
            {'name': 'recording', 'labels': ['male', 'child']}]}
        cfg_obj2 = {'filters': [
            {'name': 'recording', 'labels': ['male', 'child'], 'threshold': 'test'}]}

        with self.assertRaises(AppValidatortError) as e1:
            validate_filters(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            validate_filters(cfg_obj2)

        self.assertEqual(
            "Threshold field not found in filter", str(
                e1.exception))
        self.assertEqual(
            "Found threshold field in filter, but it is not a number", str(
                e2.exception))

    def test_actions(self):
        cfg_obj1 = {'actions': [{'name': 'start_recording',
                                 'type': 'recording',
                                 'lenght': 10,
                                 'location': '/path'},
                                {'name': 'log_event',
                                 'type': 'logging',
                                 'location': '/tmp/log.xls'}]}
        cfg_obj2 = {'streams': 'test1', 'triggers': 'test2'}
        cfg_obj3 = {'actions': 'test'}

        actions_list = ['start_recording', 'log_event']

        actions_validate = validate_actions(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e1:
            validate_actions(cfg_obj2)

        with self.assertRaises(AppValidatortError) as e2:
            validate_actions(cfg_obj3)

        self.assertEqual(actions_list, actions_validate)
        self.assertEqual("Actions field not found", str(e1.exception))
        self.assertEqual(
            "Found actions field, but is is not a list", str(
                e2.exception))

    def test_actions_name_errors(self):
        cfg_obj1 = {'actions': [
            {'test': 'start_recording', 'type': 'recording', 'lenght': 10, 'location': '/path'}]}
        cfg_obj2 = {'actions': [
            {'name': 0, 'type': 'recording', 'lenght': 10, 'location': '/path'}]}

        with self.assertRaises(AppValidatortError) as e1:
            validate_actions(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            validate_actions(cfg_obj2)

        self.assertEqual(
            "Name field not found in action", str(
                e1.exception))
        self.assertEqual(
            "Found name field in action, but it is not a string", str(
                e2.exception))

    def test_actions_type_errors(self):
        cfg_obj1 = {'actions': [
            {'name': 'start_recording', 'test': 'recording', 'lenght': 10, 'location': '/path'}]}
        cfg_obj2 = {'actions': [{'name': 'start_recording', 'type': [
            'test'], 'lenght': 10, 'location': '/path'}]}
        cfg_obj3 = {'actions': [
            {'name': 'start_recording', 'type': 'recording', 'test': 10, 'location': '/path'}]}
        cfg_obj4 = {'actions': [{'name': 'start_recording',
                                 'type': 'recording',
                                 'lenght': '10',
                                 'location': '/path'}]}

        with self.assertRaises(AppValidatortError) as e1:
            validate_actions(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            validate_actions(cfg_obj2)

        with self.assertRaises(AppValidatortError) as e3:
            validate_actions(cfg_obj3)

        with self.assertRaises(AppValidatortError) as e4:
            validate_actions(cfg_obj4)

        self.assertEqual(
            "Type field not found in action", str(
                e1.exception))
        self.assertEqual(
            "Found type field in action, but it is not a string", str(
                e2.exception))
        self.assertEqual(
            "Lenght field not found in action of type recording", str(
                e3.exception))
        self.assertEqual(
            "Lenght field in action must be a whole number", str(
                e4.exception))

    def test_actions_location_errors(self):
        cfg_obj1 = {'actions': [{'name': 'start_recording',
                                 'type': 'recording',
                                 'lenght': 10,
                                 'test': '/tmp/recording%d.mp4'}]}
        cfg_obj2 = {'actions': [
            {'name': 'start_recording', 'type': 'recording', 'lenght': 10, 'location': 0}]}

        with self.assertRaises(AppValidatortError) as e1:
            validate_actions(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            validate_actions(cfg_obj2)

        self.assertEqual(
            "Location field not found in action", str(
                e1.exception))
        self.assertEqual(
            "Found location field in action, but it is not a string", str(
                e2.exception))

    def test_triggers(self):
        cfg_obj1 = {
            'triggers': [
                {'name': 'person_recording',
                    'action': 'start_recording',
                    'filters': [
                        'person_filter',
                        'animal_filter']}]}
        cfg_obj2 = {'test': [{'name': 'person_recording',
                              'action': 'start_recording',
                              'filters': ['person_filter',
                                          'animal_filter']}]}
        cfg_obj3 = {'triggers': None}

        triggers_list = ['person_recording']
        filters_list = ['person_filter', 'animal_filter']
        actions_list = ['start_recording']

        triggers_validate = validate_triggers(
            cfg_obj1, actions_list, filters_list)

        with self.assertRaises(AppValidatortError) as e1:
            validate_triggers(cfg_obj2, actions_list, filters_list)

        with self.assertRaises(AppValidatortError) as e2:
            validate_triggers(cfg_obj3, actions_list, filters_list)

        self.assertEqual(triggers_list, triggers_validate)
        self.assertEqual("Triggers field not found", str(e1.exception))
        self.assertEqual(
            "Found triggers field, but is is not a list", str(
                e2.exception))

    def test_triggers_name_errors(self):
        cfg_obj1 = {
            'triggers': [
                {
                    'test': 'person_recording',
                    'action': 'start_recording',
                    'filters': [
                        'person_filter',
                        'animal_filter']}]}
        cfg_obj2 = {'triggers': [{'name': None,
                                  'action': 'start_recording',
                                  'filters': ['person_filter',
                                              'animal_filter']}]}

        filters_list = ['person_filter', 'animal_filter']
        actions_list = ['start_recording']

        with self.assertRaises(AppValidatortError) as e1:
            validate_triggers(cfg_obj1, actions_list, filters_list)

        with self.assertRaises(AppValidatortError) as e2:
            validate_triggers(cfg_obj2, actions_list, filters_list)

        self.assertEqual(
            "Name field not found in trigger", str(
                e1.exception))
        self.assertEqual(
            "Found name field in action, but it is not a string", str(
                e2.exception))

    def test_triggers_action_errors(self):
        cfg_obj1 = {
            'triggers': [
                {
                    'name': 'person_recording',
                    'test': 'start_recording',
                    'filters': [
                        'person_filter',
                        'animal_filter']}]}
        cfg_obj2 = {'triggers': [{'name': 'person_recording', 'action': None, 'filters': [
            'person_filter', 'animal_filter']}]}
        cfg_obj3 = {'triggers': [{'name': 'person_recording', 'action': 'test', 'filters': [
            'person_filter', 'animal_filter']}]}

        filters_list = ['person_filter', 'animal_filter']
        actions_list = ['start_recording']

        with self.assertRaises(AppValidatortError) as e1:
            validate_triggers(cfg_obj1, actions_list, filters_list)

        with self.assertRaises(AppValidatortError) as e2:
            validate_triggers(cfg_obj2, actions_list, filters_list)

        with self.assertRaises(AppValidatortError) as e3:
            validate_triggers(cfg_obj3, actions_list, filters_list)

        self.assertEqual(
            "Action field not found in trigger", str(
                e1.exception))
        self.assertEqual(
            "Found action field in trigger, but it is not a string", str(
                e2.exception))
        self.assertEqual(
            "Trigger has a not defined action", str(
                e3.exception))

    def test_trigger_filters_errors(self):
        cfg_obj1 = {
            'triggers': [
                {
                    'name': 'person_recording',
                    'action': 'start_recording',
                    'test': [
                        'person_filter',
                        'animal_filter']}]}
        cfg_obj2 = {'triggers': [
            {'name': 'person_recording', 'action': 'start_recording', 'filters': 'test'}]}
        cfg_obj3 = {
            'triggers': [
                {
                    'name': 'person_recording',
                    'action': 'start_recording',
                    'filters': [
                        0,
                        'animal_filter']}]}
        cfg_obj4 = {
            'triggers': [
                {'name': 'person_recording',
                    'action': 'start_recording',
                    'filters': [
                        'test',
                        'animal_filter']}]}

        filters_list = ['person_filter', 'animal_filter']
        actions_list = ['start_recording']

        with self.assertRaises(AppValidatortError) as e1:
            validate_triggers(cfg_obj1, actions_list, filters_list)

        with self.assertRaises(AppValidatortError) as e2:
            validate_triggers(cfg_obj2, actions_list, filters_list)

        with self.assertRaises(AppValidatortError) as e3:
            validate_triggers(cfg_obj3, actions_list, filters_list)
        with self.assertRaises(AppValidatortError) as e4:
            validate_triggers(cfg_obj4, actions_list, filters_list)

        self.assertEqual(
            "Filters field not found in trigger", str(
                e1.exception))
        self.assertEqual(
            "Found filters field in trigger, but it is not a list", str(
                e2.exception))
        self.assertEqual(
            "Found filter element in trigger, but it is not a string", str(
                e3.exception))
        self.assertEqual(
            "Trigger has a not defined filter", str(
                e4.exception))

    def test_validate(self):
        self.validator = AppValidator()
        cfg = {'streams': [{'id': 'stream0',
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

        validate = self.validator.validate(cfg)

        self.assertEqual(None, validate)


if __name__ == '__main__':
    unittest.main()
