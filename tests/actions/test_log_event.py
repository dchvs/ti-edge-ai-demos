#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import unittest

from rr.actions.log_event import LogEvent, LogEventError, log, validate_csv


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


class TestLogEventSuccess(unittest.TestCase):

    def setUp(self):
        media = mockMedia('test_media_name')
        image = mockImage('2021-07-27 12:00:20')

    def test_validate_csv_success(self):
        csv_file = 'test_path/test.csv'
        validate_good = validate_csv(csv_file)

        self.assertEqual(csv_file, validate_good)

    def test_validate_csv_error(self):
        csv_file = 'test_path/test.txt'

        with self.assertRaises(LogEventError) as e:
            validate_fail = validate_csv(csv_file)

        self.assertEqual(
            "The file used for logging must have a .csv file extension", str(
                e.exception))


if __name__ == '__main__':
    unittest.main()
