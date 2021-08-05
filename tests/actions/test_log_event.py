#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import unittest

import csv
import os
from rr.actions.log_event import LogEvent, LogEventError


class mockMedia():
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name


class mockImage():
    def __init__(self, timestamp):
        self._timestamp = timestamp

    def get_timestamp(self):
        return self._timestamp


class TestLogEvent(unittest.TestCase):
    csv_file_good = 'tests/actions/test_log.csv'

    def setUp(self):
        if os.path.exists(self.csv_file_good):
            os.remove(self.csv_file_good)

    def test_log_success(self):
        media = mockMedia('test_media_name')
        image = mockImage('2021-07-27 12:00:20')
        inf_results = {
            "instances": [
                {
                    "labels": [
                        {
                            "label": 'ZZZZ', "probability": 0.99}, {
                            "label": 'AAAA', "probability": 0.01}, ], "bbox": {
                        "x": 'X', "y": 'Y', "width": 'width', "height": 'height'}}, {
                    "labels": [
                        {
                            "label": 'XXXX', "probability": 0.97}, {
                            "label": 'WWWW', "probability": 0.01}, ], "bbox": {
                        "x": 'X', "y": 'Y', "width": 'width', "height": 'height'}}]}

        log_action = LogEvent(self.csv_file_good)
        log_action.execute(media, image, inf_results)

        first_row_ret = [
            'test_media_name',
            '2021-07-27 12:00:20',
            'ZZZZ',
            '0.99',
            'X',
            'Y',
            'width',
            'height']

        second_row_ret = [
            'test_media_name',
            '2021-07-27 12:00:20',
            'XXXX',
            '0.97',
            'X',
            'Y',
            'width',
            'height']

        with open(self.csv_file_good) as f:
            reader = csv.reader(f)
            self.assertEqual(log_action._fieldnames, next(reader))
            self.assertEqual(first_row_ret, next(reader))
            self.assertEqual(second_row_ret, next(reader))

    def test_log_no_parent_dir(self):
        no_parent = 'tests/actions/no/parent/dir/test_log.csv'

        with self.assertRaises(LogEventError) as e:
            log_action = LogEvent(no_parent)

        self.assertEqual(
            "Unable to open logging events file for writing", str(
                e.exception))

    def test_log_non_writable(self):
        no_parent = '/'

        with self.assertRaises(LogEventError) as e:
            log_action = LogEvent(no_parent)

        self.assertEqual(
            "Unable to open logging events file for writing", str(
                e.exception))


if __name__ == '__main__':
    unittest.main()
