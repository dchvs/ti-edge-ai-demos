#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from gstreamer.gstmedia import *
import unittest


class TestGstMedia(unittest.TestCase):
    def testCreatePipeline(self):
        desc = "videotestsrc ! fakesink"

        gstmedia = GstMedia()

        ret = gstmedia.CreatePipeline(desc)
        assert(ret is not None)
        assert(gstmedia.GetPipeline() is not None)

    def testDeletePipeline(self):
        desc = "videotestsrc ! fakesink"

        gstmedia = GstMedia()

        ret = gstmedia.CreatePipeline(desc)
        ret = gstmedia.DeletePipeline()
        assert(ret is True)

    def testPlayPipeline(self):
        desc = "videotestsrc ! fakesink async=false"

        gstmedia = GstMedia()

        ret = gstmedia.CreatePipeline(desc)

        self.assertEqual(
            gst.State.NULL,
            gstmedia.GetPipeline().get_state(
                gst.CLOCK_TIME_NONE)[1])
        gstmedia.PlayPipeline()
        self.assertEqual(
            gst.State.PLAYING,
            gstmedia.GetPipeline().get_state(
                gst.CLOCK_TIME_NONE)[1])

    def testStopPipeline(self):
        desc = "videotestsrc ! fakesink async=false"

        gstmedia = GstMedia()

        ret = gstmedia.CreatePipeline(desc)

        gstmedia.PlayPipeline()
        self.assertEqual(
            gst.State.PLAYING,
            gstmedia.GetPipeline().get_state(
                gst.CLOCK_TIME_NONE)[1])
        gstmedia.StopPipeline()
        self.assertEqual(
            gst.State.NULL,
            gstmedia.GetPipeline().get_state(
                gst.CLOCK_TIME_NONE)[1])

    def testDeleteMultipleTimes(self):
        desc = "videotestsrc ! fakesink async=false"

        gstmedia = GstMedia()

        ret = gstmedia.CreatePipeline(desc)

        ret = gstmedia.DeletePipeline()
        ret = gstmedia.DeletePipeline()

        assert(ret is True)


if __name__ == '__main__':
    unittest.main()
