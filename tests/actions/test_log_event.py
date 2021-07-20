#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import unittest

import csv
from rr.actions.log_event import LogEvent, LogEventError, log, validate_csv, set_file_headers


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
        csv_file_good = 'test_path/test.csv'
        validate_good = validate_csv(csv_file_good)

        self.assertEqual(csv_file_good, validate_good)

    def test_validate_csv_error(self):
        csv_file_invalid = 'test_path/test.txt'

        with self.assertRaises(LogEventError) as e:
            validate_fail = validate_csv(csv_file_invalid)

        self.assertEqual(
            "The file used for logging must have a .csv file extension", str(
                e.exception))

    def test_set_header_success(self):
        csv_file_good = 'tests/actions/test_headers.csv'
        fieldnames = [
            'name',
            'time',
            'label',
            'probability',
            'bbox-x',
            'bbox-y',
            'bbox-width',
            'bbox-height']

        result_fieldname = set_file_headers(csv_file_good)

        with open(csv_file_good) as f:
            reader = csv.reader(f)
            first_line = next(reader)

        self.assertEqual(fieldnames, first_line)
        self.assertEqual(fieldnames, result_fieldname)


if __name__ == '__main__':
    unittest.main()
