#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import numpy as np
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


class MockTriggerMedia:
    pass


model = "/opt/edge_ai_apps/models/detection/TFL-OD-200-ssd-mobV1-coco-mlperf-300x300/"
disp_width = 2040
disp_height = 1920
default_width = 320
default_height = 240
default_dimentions = 3


class MockImage:
    def __init__():
        pass

    def get_mock_image():
        return np.zeros(
            (default_width *
             default_height *
             default_dimentions),
            np.uint8)


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
        ai_manager = AIManagerOnNewImage(model, disp_width, disp_height)

        desc = "videotestsrc num-buffers=1 is-live=true ! video/x-raw,width=320,height=240,format=BGRx ! appsink name=appsink async=false emit-signals=true"
        key = "media1"

        media = GstMedia()
        media.create_media(desc)

        media_manager = MediaManager()
        media_manager.add_media(key, media)

        # ActionManager setup
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
        mock_image = MockImage.get_mock_image()
        action_manager.execute = MagicMock(prediction, mock_image, media)

        stream_manager = StreamManager(
            action_manager,
            ai_manager,
            media_manager,
            model,
            disp_width,
            disp_height)

        stream_manager.play()
        time.sleep(1)

        action_manager.execute.assert_called_once()


if __name__ == '__main__':
    unittest.main()
