#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from gi.repository import Gst as gst
from gstreamer.gstmedia import GstMedia
import unittest


class TestGstMedia(unittest.TestCase):
    def testCreateMedia(self):
        desc = "videotestsrc ! fakesink"

        gstmedia = GstMedia()

        ret = gstmedia.CreateMedia(desc)
        self.assertTrue(ret)
        assert(gstmedia.GetMedia() is not None)

    def testDeleteMedia(self):
        desc = "videotestsrc ! fakesink"

        gstmedia = GstMedia()

        gstmedia.CreateMedia(desc)
        ret = gstmedia.DeleteMedia()
        assert(ret is True)

    def testPlayMedia(self):
        desc = "videotestsrc ! fakesink async=false"

        gstmedia = GstMedia()

        gstmedia.CreateMedia(desc)

        self.assertEqual(
            gst.State.NULL,
            gstmedia.GetMedia().get_state(
                gst.CLOCK_TIME_NONE)[1])
        gstmedia.PlayMedia()
        self.assertEqual(
            gst.State.PLAYING,
            gstmedia.GetMedia().get_state(
                gst.CLOCK_TIME_NONE)[1])

    def testStopMedia(self):
        desc = "videotestsrc ! fakesink async=false"

        gstmedia = GstMedia()

        gstmedia.CreateMedia(desc)

        gstmedia.PlayMedia()
        self.assertEqual(
            gst.State.PLAYING,
            gstmedia.GetMedia().get_state(
                gst.CLOCK_TIME_NONE)[1])
        gstmedia.StopMedia()
        self.assertEqual(
            gst.State.NULL,
            gstmedia.GetMedia().get_state(
                gst.CLOCK_TIME_NONE)[1])

    def testDeleteMultipleTimes(self):
        desc = "videotestsrc ! fakesink async=false"

        gstmedia = GstMedia()

        gstmedia.CreateMedia(desc)

        gstmedia.DeleteMedia()
        ret = gstmedia.DeleteMedia()

        assert(ret is True)


if __name__ == '__main__':
    unittest.main()
