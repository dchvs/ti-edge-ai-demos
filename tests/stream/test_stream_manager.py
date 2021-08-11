#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import time
import unittest
from unittest.mock import MagicMock

from rr.actions.action_manager import ActionManager
from rr.actions.action_manager import Trigger, TriggerError
from rr.ai.ai_manager import AIManagerOnNewImage
from rr.gstreamer.gst_media import GstMedia
from rr.gstreamer.media_manager import MediaManager
from rr.stream.stream_manager import OnNewImage
from rr.stream.stream_manager import StreamManager


class MockImage:
    pass


class MockTriggerMedia:
    pass


model = "/opt/edge_ai_apps/models/detection/TFL-OD-200-ssd-mobV1-coco-mlperf-300x300/"
disp_width = 2040
disp_height = 1920
mock_image = MockImage()
mock_trigger_media = MockTriggerMedia()


class MockTriggerFilter1:
    def __init__(self):
        self.apply = MagicMock()

    def get_name(self):
        return "mock_filter1"


class MockTriggerFilter2:
    def __init__(self):
        self.apply = MagicMock()

    def get_name(self):
        return "mock_filter2"


class MockTriggerAction:
    def __init__(self):
        self.execute = MagicMock()

    def get_name(self):
        return "mock_action"


class TestStreamManager(unittest.TestCase):
    def testsuccess(self):

        self.desc = {
            "name": "trigger_name",
            "action": "mock_action",
            "filters": [
                "mock_filter1",
                "mock_filter2",
            ]
        }

        self.action = MockTriggerAction()
        self.filter1 = MockTriggerFilter1()
        self.filter2 = MockTriggerFilter2()
        self.filters = [self.filter1, self.filter2]

        trigger = Trigger(self.desc, self.action, self.filters)
        action_manager = ActionManager(trigger)

        prediction = {"mock": "prediction"}
        action_manager.execute = MagicMock(
            prediction, mock_image, mock_trigger_media)

        self.mock_on_new_prediction_cb = MagicMock()
        self.mock_on_new_postprocess_cb = MagicMock()

        ai_manager = AIManagerOnNewImage(model, disp_width, disp_height,
                                         self.mock_on_new_prediction_cb,
                                         self.mock_on_new_postprocess_cb)

        ai_manager.process_image = MagicMock(
            mock_image, model, disp_width, disp_height)

        desc = "videotestsrc num-buffers=1 is-live=true ! video/x-raw,width=640,height=480,format=BGRx ! appsink name=appsink async=false emit-signals=true"
        key = "media1"

        media = GstMedia()
        media.create_media(desc)

        media_manager = MediaManager()
        media_manager.add_media(key, media)

        stream_manager = StreamManager(
            action_manager,
            ai_manager,
            media_manager,
            model,
            disp_width,
            disp_height)

        stream_manager.play()
        time.sleep(1)
        ai_manager.process_image.assert_called_once()
        action_manager.execute.assert_called_once()


if __name__ == '__main__':
    unittest.main()
