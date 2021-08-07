#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import gi  # nopep8
gi.require_version('Gst', '1.0')  # nopep8
gi.require_version('GLib', '2.0')  # nopep8
from gi.repository import Gst as gst
from gi.repository import GLib

import unittest

from rr.display.display_manager import DisplayManager
from rr.display.display_manager import DisplayManagerError

def _get_media_State(media):
    return media.get_state(gst.CLOCK_TIME_NONE)[1]


class TestDisplayManager(unittest.TestCase):
    def setUp(self):
        self.display_manager = DisplayManager()
        self.stream_name = "stream0"
        self.display_manager.add_stream(self.stream_name)
        self.display_media = self.display_manager._get_media()

    def test_add_stream(self):
        list = self.display_manager._get_stream_list()
        self.assertTrue(self.stream_name in list)

    def test_remove_stream(self):
        self.display_manager.remove_stream(self.stream_name)
        list = self.display_manager._get_stream_list()
        self.assertTrue(self.stream_name not in list)

    def test_create_display(self):
        display_desc = "videomixer name=mixer  sink_0::xpos=0 sink_0::ypos=0 ! queue ! xvimagesink sync=false async=false  interpipesrc listen-to=stream0 format=time ! queue ! videoscale ! video/x-raw,width=320,height=240 ! mixer. "
        self.display_manager.create_display()
        self.assertEqual(display_desc, self.display_manager._get_display_desc())

    def test_play_display(self):
        self.test_create_display()
        media_state = _get_media_State(self.display_media.get_media())
        self.assertEqual(gst.State.NULL, media_state)
        self.display_manager.play_display()
        media_state = _get_media_State(self.display_media.get_media())
        self.assertEqual(gst.State.PLAYING, media_state)

    def test_stop_display(self):
        self.test_play_display()
        display_media = self.display_manager._get_media()
        self.display_manager.stop_display()
        media_state = _get_media_State(self.display_media.get_media())
        self.assertEqual(gst.State.NULL, media_state)

    def test_delete_display(self):
        self.test_create_display()
        self.display_manager.delete_display()
        self.assertEqual(None, self.display_manager._get_display_desc())

    def test_full_sequence(self):
        self.test_stop_display()
        self.display_manager.stop_display()
        self.display_manager.delete_display()
        self.assertEqual(None, self.display_manager._get_display_desc())

class TestDisplayManagerFail(unittest.TestCase):
    def setUp(self):
        self.display_manager = DisplayManager()
        self.stream_name = "stream0"
        self.display_manager.add_stream(self.stream_name)

    def test_add_stream_none(self):
        with self.assertRaisesRegex(DisplayManagerError, "Invalid key"):
            self.display_manager.add_stream(None)

    def test_add_stream_not_string(self):
        with self.assertRaisesRegex(DisplayManagerError, "Invalid key"):
            self.display_manager.add_stream(1)
            
    def test_add_stream_duplicated(self):
        with self.assertRaisesRegex(DisplayManagerError, "Stream already exists in display manager"):
            self.display_manager.add_stream(self.stream_name)

    def test_add_stream_after_created(self):
        self.display_manager.create_display()
        with self.assertRaisesRegex(DisplayManagerError, "Display already created, delete before adding a new stream"):
            self.display_manager.add_stream("stream1")

    def test_add_stream_exceed_limit(self):
        self.display_manager.add_stream("stream1")
        self.display_manager.add_stream("stream2")
        self.display_manager.add_stream("stream3")
        self.display_manager.add_stream("stream4")
        self.display_manager.add_stream("stream5")
        self.display_manager.add_stream("stream6")
        self.display_manager.add_stream("stream7")
        with self.assertRaisesRegex(DisplayManagerError, "Max number of streams reached"):
            self.display_manager.add_stream("stream8")
            
    def test_remove_stream_none(self):
        with self.assertRaisesRegex(DisplayManagerError, "Invalid key"):
            self.display_manager.remove_stream(None)

    def test_remove_stream_not_string(self):
        with self.assertRaisesRegex(DisplayManagerError, "Invalid key"):
            self.display_manager.remove_stream(1)

    def test_remove_stream_invalid(self):
        with self.assertRaisesRegex(DisplayManagerError, "Stream doesn't exist in display manager"):
            self.display_manager.remove_stream("stream1")

    def test_remove_stream_after_created(self):
        self.display_manager.create_display()
        with self.assertRaisesRegex(DisplayManagerError, "Display already created, delete before removing a stream"):
            self.display_manager.remove_stream(self.stream_name)

    def test_create_display_empty(self):
        self.display_manager.remove_stream(self.stream_name)
        with self.assertRaisesRegex(DisplayManagerError, "No streams added"):
            self.display_manager.create_display()

    def test_create_display_duplicated(self):
        self.display_manager.create_display()
        with self.assertRaisesRegex(DisplayManagerError, "Display already created"):
            self.display_manager.create_display()

    def test_play_display_not_created(self):
        with self.assertRaisesRegex(DisplayManagerError, "Display description not created yet"):
            self.display_manager.play_display()

    def test_stop_display_not_created(self):
        with self.assertRaisesRegex(DisplayManagerError, "Display description not created yet"):
            self.display_manager.stop_display()

    def test_delete_display_not_created(self):
        with self.assertRaisesRegex(DisplayManagerError, "Display description not created yet"):
            self.display_manager.stop_display()

if __name__ == '__main__':
    unittest.main()
