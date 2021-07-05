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


if __name__ == '__main__':
    unittest.main()
