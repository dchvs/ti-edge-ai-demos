#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import unittest

from rr.config.app_validator import AppValidator, AppValidatortError


class TestYamlFormat(unittest.TestCase):

    def setUp(self):
        self.validator = AppValidator()

    def test_streams(self):
        cfg_obj1 = {'streams': [
            {'id': 'stream0', 'uri': 'http0', 'triggers': ['person_recording']}]}
        cfg_obj2 = {'triggers': 'test', 'filters': 0}
        cfg_obj3 = {'streams': 'test'}

        streams_validate = self.validator.validate_streams(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_streams(cfg_obj2)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_streams(cfg_obj3)

        self.assertEqual(None, streams_validate)
        self.assertEqual("streams object not found", str(e1.exception))
        self.assertEqual("Invalid streams format", str(e2.exception))

    def test_id_errors(self):
        cfg_obj1 = {'streams': [
            {'test': 'stream0', 'uri': 'http0', 'triggers': ['person_recording']}]}
        cfg_obj2 = {'streams': [
            {'id': 0, 'uri': 'http0', 'triggers': ['person_recording']}]}

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_streams(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_streams(cfg_obj2)

        self.assertEqual("id property not found in stream", str(e1.exception))
        self.assertEqual("Invalid id format", str(e2.exception))

    def test_uri_errors(self):
        cfg_obj1 = {'streams': [
            {'id': 'stream0', 'test': 'http0', 'triggers': ['person_recording']}]}
        cfg_obj2 = {'streams': [
            {'id': 'stream0', 'uri': 0, 'triggers': ['person_recording']}]}

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_streams(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_streams(cfg_obj2)

        self.assertEqual("uri property not found in stream", str(e1.exception))
        self.assertEqual("Invalid uri format", str(e2.exception))

    def test_triggers_errors(self):
        cfg_obj1 = {'streams': [
            {'id': 'stream0', 'uri': 'http0', 'test': ['person_recording']}]}
        cfg_obj2 = {'streams': [
            {'id': 'stream0', 'uri': "http0", 'triggers': 'test'}]}

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_streams(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_streams(cfg_obj2)

        self.assertEqual(
            "triggers property not found in stream", str(
                e1.exception))
        self.assertEqual("Invalid triggers format", str(e2.exception))

    def test_filters(self):
        cfg_obj1 = {'filters': [{'name': 'person_filter',
                                 'labels': ['male', 'child'], 'threshold': 0.7}]}
        cfg_obj2 = {'streams': 'test1', 'triggers': 'test2'}
        cfg_obj3 = {'filters': 'test'}

        filters_validate = self.validator.validate_filters(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_filters(cfg_obj2)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_filters(cfg_obj3)

        self.assertEqual(None, filters_validate)
        self.assertEqual("filters object not found", str(e1.exception))
        self.assertEqual("Invalid filters format", str(e2.exception))

    def test_filters_name_errors(self):
        cfg_obj1 = {'filters': [
            {'labels': ['male', 'child'], 'threshold': 0.7}]}
        cfg_obj2 = {'filters': [
            {'name': [], 'labels': ['male', 'child'], 'threshold': 0.7}]}

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_filters(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_filters(cfg_obj2)

        self.assertEqual(
            "name property not found in filter", str(
                e1.exception))
        self.assertEqual("Invalid name format in filter", str(e2.exception))

    def test_labels_errors(self):
        cfg_obj1 = {'filters': [{'name': 'recording',
                                 'test': ['male', 'child'], 'threshold': 0.7}]}
        cfg_obj2 = {'filters': [
            {'name': 'recording', 'labels': 'test', 'threshold': 0.7}]}
        cfg_obj3 = {'filters': [{'name': 'recording',
                                 'labels': [0, 'child'], 'threshold': 0.7}]}

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_filters(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_filters(cfg_obj2)

        with self.assertRaises(AppValidatortError) as e3:
            self.validator.validate_filters(cfg_obj3)

        self.assertEqual(
            "labels property not found in filter", str(
                e1.exception))
        self.assertEqual("Invalid labels format in filter", str(e2.exception))
        self.assertEqual(
            "Invalid label format in filter labels", str(
                e3.exception))

    def test_threshold_errors(self):
        cfg_obj1 = {'filters': [
            {'name': 'recording', 'labels': ['male', 'child']}]}
        cfg_obj2 = {'filters': [
            {'name': 'recording', 'labels': ['male', 'child'], 'threshold': 'test'}]}

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_filters(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_filters(cfg_obj2)

        self.assertEqual(
            "threshold property not found in filter", str(
                e1.exception))
        self.assertEqual("Invalid threshold format", str(e2.exception))

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

        actions_validate = self.validator.validate_actions(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_actions(cfg_obj2)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_actions(cfg_obj3)

        self.assertEqual(None, actions_validate)
        self.assertEqual("actions object not found", str(e1.exception))
        self.assertEqual("Invalid actions format", str(e2.exception))

    def test_actions_name_errors(self):
        cfg_obj1 = {'actions': [
            {'test': 'start_recording', 'type': 'recording', 'lenght': 10, 'location': '/path'}]}
        cfg_obj2 = {'actions': [
            {'name': 0, 'type': 'recording', 'lenght': 10, 'location': '/path'}]}

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_actions(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_actions(cfg_obj2)

        self.assertEqual(
            "name property not found in action", str(
                e1.exception))
        self.assertEqual("Invalid name format in action", str(e2.exception))

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
            self.validator.validate_actions(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_actions(cfg_obj2)

        with self.assertRaises(AppValidatortError) as e3:
            self.validator.validate_actions(cfg_obj3)

        with self.assertRaises(AppValidatortError) as e4:
            self.validator.validate_actions(cfg_obj4)

        self.assertEqual(
            "type property not found in action", str(
                e1.exception))
        self.assertEqual("Invalid type format in action", str(e2.exception))
        self.assertEqual(
            "lenght property not found in action of type recording", str(
                e3.exception))
        self.assertEqual(
            "Invalid lenght format in action of type recording", str(
                e4.exception))

    def test_actions_location_errors(self):
        cfg_obj1 = {'actions': [{'name': 'start_recording',
                                 'type': 'recording',
                                 'lenght': 10,
                                 'test': '/tmp/recording%d.mp4'}]}
        cfg_obj2 = {'actions': [
            {'name': 'start_recording', 'type': 'recording', 'lenght': 10, 'location': 0}]}

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_actions(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_actions(cfg_obj2)

        self.assertEqual(
            "location property not found in action", str(
                e1.exception))
        self.assertEqual(
            "Invalid location format in action", str(
                e2.exception))

    def test_triggers(self):
        cfg_obj1 = {
            'triggers': [
                {
                    'name': 'person_recording',
                    'action': 'start_recording',
                    'filters': [
                        'person_filter',
                        'animal_filter']}]}
        cfg_obj2 = {'test': [{'name': 'person_recording',
                              'action': 'start_recording',
                              'filters': ['person_filter',
                                          'animal_filter']}]}
        cfg_obj3 = {'triggers': None}

        triggers_validate = self.validator.validate_triggers(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_triggers(cfg_obj2)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_triggers(cfg_obj3)

        self.assertEqual(None, triggers_validate)
        self.assertEqual("triggers object not found", str(e1.exception))
        self.assertEqual("Invalid triggers format", str(e2.exception))

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

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_triggers(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_triggers(cfg_obj2)

        self.assertEqual(
            "name property not found in triggers", str(
                e1.exception))
        self.assertEqual("Invalid name format in triggers", str(e2.exception))

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

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_triggers(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_triggers(cfg_obj2)

        self.assertEqual(
            "action property not found in triggers", str(
                e1.exception))
        self.assertEqual(
            "Invalid action format in triggers", str(
                e2.exception))

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

        with self.assertRaises(AppValidatortError) as e1:
            self.validator.validate_triggers(cfg_obj1)

        with self.assertRaises(AppValidatortError) as e2:
            self.validator.validate_triggers(cfg_obj2)

        with self.assertRaises(AppValidatortError) as e3:
            self.validator.validate_triggers(cfg_obj3)

        self.assertEqual(
            "filters property not found in triggers", str(
                e1.exception))
        self.assertEqual(
            "Invalid filters format in triggers", str(
                e2.exception))
        self.assertEqual(
            "Invalid filter format in triggers filters", str(
                e3.exception))


if __name__ == '__main__':
    unittest.main()
