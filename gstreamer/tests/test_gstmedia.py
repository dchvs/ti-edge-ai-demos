#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from gi.repository import Gst as gst
from gstreamer.gstmedia import GstMedia
import unittest


def _GetMediaState(media):
    return media.get_state(gst.CLOCK_TIME_NONE)[1]


class TestGstMedia(unittest.TestCase):
    def setUp(self):
        self.desc = "videotestsrc ! fakesink"

        self.gstmedia = GstMedia()

        self.ret = self.gstmedia.CreateMedia(self.desc)

    def testCreateMedia(self):
        self.assertTrue(self.ret)

    def testDeleteMedia(self):
        ret = self.gstmedia.DeleteMedia()
        assert(ret is True)

    def testPlayMedia(self):
        media_state = _GetMediaState(self.gstmedia.GetMedia())
        self.assertEqual(gst.State.NULL, media_state)

        ret = self.gstmedia.PlayMedia()
        assert(ret is True)

        media_state = _GetMediaState(self.gstmedia.GetMedia())
        self.assertEqual(gst.State.PLAYING, media_state)

    def testStopMedia(self):
        self.gstmedia.PlayMedia()
        media_state = _GetMediaState(self.gstmedia.GetMedia())
        self.assertEqual(gst.State.PLAYING, media_state)

        ret = self.gstmedia.StopMedia()
        assert(ret is True)

        media_state = _GetMediaState(self.gstmedia.GetMedia())
        self.assertEqual(gst.State.NULL, media_state)

    def testDeleteMultipleTimes(self):
        self.gstmedia.DeleteMedia()
        ret = self.gstmedia.DeleteMedia()

        assert(ret is True)


if __name__ == '__main__':
    unittest.main()
