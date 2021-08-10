#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import unittest

from rr.actions.record_event import RecordEvent

media_name = "media0"
timestamp = '2021-07-27-12:00:20'


class mockMedia():
    def get_name(self):
        return media_name


class MockImage():
    def get_timestamp(self):
        return timestamp


class MockFilter():
    def __init__(self):
        self.enable_buffer_flow = False

    def set_enabled(self, status):
        self.enable_buffer_flow = status


class TestRecordEvent(unittest.TestCase):

    def test_record_event_success(self):
        rec_time = 3.0

        event_rec = RecordEvent('/tmp')
        event_rec.execute(mockMedia(), MockImage(), rec_time, MockFilter())
        event_rec.execute(mockMedia(), MockImage(), rec_time, MockFilter())


if __name__ == '__main__':
    unittest.main()
