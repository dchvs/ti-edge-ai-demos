#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from gstreamer.media_manager import *
import unittest


class TestGstManager(unittest.TestCase):
    def testCreatePipeline(self):
        desc = "videotestsrc ! fakesink"

        gst_manager = GstManager()

        ret = gst_manager.CreatePipeline(desc)
        assert(ret is not None)
        assert(gst_manager.pipeline is not None)

    def testDeletePipeline(self):
        desc = "videotestsrc ! fakesink"

        gst_manager = GstManager()

        ret = gst_manager.CreatePipeline(desc)
        ret = gst_manager.DeletePipeline()
        assert(ret is True)

    def testPlayPipeline(self):
        desc = "videotestsrc ! fakesink async=false"

        gst_manager = GstManager()

        ret = gst_manager.CreatePipeline(desc)

        self.assertEqual(
            gst.State.NULL,
            gst_manager.pipeline.get_state(
                gst.CLOCK_TIME_NONE)[1])
        gst_manager.PlayPipeline()
        self.assertEqual(
            gst.State.PLAYING,
            gst_manager.pipeline.get_state(
                gst.CLOCK_TIME_NONE)[1])

    def testStopPipeline(self):
        desc = "videotestsrc ! fakesink async=false"

        gst_manager = GstManager()

        ret = gst_manager.CreatePipeline(desc)

        gst_manager.PlayPipeline()
        self.assertEqual(
            gst.State.PLAYING,
            gst_manager.pipeline.get_state(
                gst.CLOCK_TIME_NONE)[1])
        gst_manager.StopPipeline()
        self.assertEqual(
            gst.State.NULL,
            gst_manager.pipeline.get_state(
                gst.CLOCK_TIME_NONE)[1])


if __name__ == '__main__':
    unittest.main()
