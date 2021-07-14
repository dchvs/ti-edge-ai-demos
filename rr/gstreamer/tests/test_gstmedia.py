#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import gi  # nopep8
gi.require_version('Gst', '1.0')  # nopep8
gi.require_version('GLib', '2.0')  # nopep8
from gi.repository import Gst as gst
from gi.repository import GLib

from rr.gstreamer.gstmedia import GstMedia
from rr.gstreamer.gstmedia import GstMediaError
import unittest


def _GetMediaState(media):
    return media.get_state(gst.CLOCK_TIME_NONE)[1]


class TestGstMedia(unittest.TestCase):
    def setUp(self):
        self.desc = "videotestsrc ! fakesink"

        self.gstmedia = GstMedia()

        self.gstmedia.CreateMedia(self.desc)

    def testCreateMedia(self):
        self.assertTrue(isinstance(self.gstmedia.GetMedia(), gst.Pipeline))

    def testDeleteMedia(self):
        self.gstmedia.DeleteMedia()
        assert self.gstmedia.GetMedia() is None, "Failed to delete the media object properly"

    def testPlayMedia(self):
        media_state = _GetMediaState(self.gstmedia.GetMedia())
        self.assertEqual(gst.State.NULL, media_state)

        self.gstmedia.PlayMedia()
        media_state = _GetMediaState(self.gstmedia.GetMedia())
        self.assertEqual(gst.State.PLAYING, media_state)

    def testStopMedia(self):
        self.gstmedia.PlayMedia()
        media_state = _GetMediaState(self.gstmedia.GetMedia())
        self.assertEqual(gst.State.PLAYING, media_state)

        self.gstmedia.StopMedia()

        media_state = _GetMediaState(self.gstmedia.GetMedia())
        self.assertEqual(gst.State.NULL, media_state)

    def testDeleteMultipleTimes(self):
        self.gstmedia.DeleteMedia()
        assert self.gstmedia.GetMedia() is None, "Failed to delete the media object properly"
        self.gstmedia.DeleteMedia()
        assert self.gstmedia.GetMedia() is None, "Failed to delete the media object properly"


class TestGstMediaFail(unittest.TestCase):
    def testCreateMedia(self):
        # Force desc to make media fail
        self.desc = "videotestsrc ! "
        self.gstmedia = GstMedia()

        with self.assertRaisesRegex(GstMediaError, "Unable to create the media"):
            self.gstmedia.CreateMedia(self.desc)

    def testPlayMedia(self):
        # Force blocking of playing state
        self.desc = "fakesrc ! fakesink async=false state-error=3"
        self.gstmedia = GstMedia()
        self.gstmedia.CreateMedia(self.desc)

        with self.assertRaisesRegex(GstMediaError, "Unable to play the media"):
            self.gstmedia.PlayMedia()

        media_state = _GetMediaState(self.gstmedia.GetMedia())
        self.assertNotEqual(gst.State.PLAYING, media_state)

    def testStopMedia(self):
        # Force blocking of stopped state
        self.desc = "fakesrc ! fakesink async=false state-error=5"
        self.gstmedia = GstMedia()
        self.gstmedia.CreateMedia(self.desc)

        self.gstmedia.PlayMedia()
        with self.assertRaisesRegex(GstMediaError, "Unable to stop the media"):
            self.gstmedia.StopMedia()

        media_state = _GetMediaState(self.gstmedia.GetMedia())
        self.assertNotEqual(gst.State.PLAYING, media_state)


if __name__ == '__main__':
    unittest.main()
