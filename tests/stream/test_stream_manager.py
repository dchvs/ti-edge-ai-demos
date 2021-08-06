#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import unittest
from unittest.mock import MagicMock

from rr.ai.ai_manager import AIManagerOnNewImage
from rr.gstreamer.imedia import IMedia
from rr.gstreamer.media_manager import MediaManager
from rr.stream.stream_manager import StreamManager
from rr.stream.stream_manager import OnNewImage


class MockImage:
    pass


model = "/opt/edge_ai_apps/models/detection/TFL-OD-200-ssd-mobV1-coco-mlperf-300x300/"
disp_width = 2040
disp_height = 1920
mock_image = MockImage()


class MockMediaManager(MediaManager):
    def install_callback(self, callback):
        self.callback = callback

    def play_media(self):
        self.callback(mock_image)


class TestStreamManager(unittest.TestCase):
    def testsuccess(self):
        self.mock_on_new_prediction_cb = MagicMock()
        self.mock_on_new_postprocess_cb = MagicMock()

        ai_manager = AIManagerOnNewImage(model, disp_width, disp_height,
                                         self.mock_on_new_prediction_cb,
                                         self.mock_on_new_postprocess_cb)

        ai_manager.process_image = MagicMock(
            mock_image, model, disp_width, disp_height)

        desc = "videotestsrc is-live=true ! fakesink async=false"
        key = "media1"

        media = IMedia()
        media.create_media(desc)

        media_manager = MockMediaManager()
        media_manager.add_media(key, media)

        stream_manager = StreamManager(ai_manager, media_manager)

        stream_manager.play()
        ai_manager.process_image.assert_called_once_with(
            mock_image, model, disp_width, disp_height)


if __name__ == '__main__':
    unittest.main()
