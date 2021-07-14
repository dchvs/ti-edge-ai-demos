#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from gi.repository import Gst as gst
from gi.repository import GLib
from gstreamer.gstmedia import GstMedia
from gstreamer.gstmedia import GstMediaError
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
        self.desc = "videotestsrc ! fakesink state-error=3"
        self.gstmedia = GstMedia()
        self.gstmedia.CreateMedia(self.desc)

        self.gstmedia.PlayMedia()
        media_state = _GetMediaState(self.gstmedia.GetMedia())
        self.assertNotEqual(gst.State.PLAYING, media_state)

    def testStopMedia(self):
        # Force blocking of stopped state
        self.desc = "fakesrc ! fakesink state-error=6"
        self.gstmedia = GstMedia()
        self.gstmedia.CreateMedia(self.desc)

        self.gstmedia.StopMedia()
        media_state = _GetMediaState(self.gstmedia.GetMedia())
        self.assertNotEqual(gst.State.PLAYING, media_state)


if __name__ == '__main__':
    unittest.main()
