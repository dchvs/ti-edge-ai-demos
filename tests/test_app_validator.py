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

    def test_filers_name_errors(self):
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


if __name__ == '__main__':
    unittest.main()
