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
from rr.config.app_config_loader import AppConfigLoader
from rr.display.display_manager import DisplayManager
from rr.gstreamer.gst_media import GstMedia
from rr.gstreamer.media_manager import MediaManager
from rr.stream.stream_manager import OnNewImage
from rr.stream.stream_manager import StreamManager
from bin.utils.imagehandler import ImageHandler


class MockTriggerMedia:
    pass

default_config_file = "config.yaml"
disp_width = 2040
disp_height = 1920
default_dimentions = 3
img_path = "./data/0004.jpg"


class MockImage:
    def __init__(self):
        img_handler = ImageHandler()
        self.real_img = img_handler.load_image(img_path)

    def get_mock_image(self):
        return self.real_img


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

        config_obj = AppConfigLoader()
        config_dict = config_obj.load(default_config_file)
        model_params = config_dict['model_params']

        model = model_params['model']['detection']
        disp_width = model_params['disp_width']
        disp_height = model_params['disp_height']

        ai_manager = AIManagerOnNewImage(model, disp_width, disp_height)

        desc = "videotestsrc num-buffers=1 is-live=true ! video/x-raw,width=320,height=240,format=BGRx ! appsink name=appsink async=false emit-signals=true"
        key = "media1"

        media = GstMedia()
        media.create_media("name", desc)

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
        action_manager = ActionManager()
        display_manager = DisplayManager()

        streams = []
        streams.append(media)
        display_manager.add_stream(media)

        prediction = {"mock": "prediction"}
        img = MockImage()
        mock_image = img.get_mock_image()
        action_manager.execute = MagicMock(prediction, mock_image, media)

        stream_manager = StreamManager(
            action_manager,
            ai_manager,
            display_manager,
            media_manager,
            model,
            disp_width,
            disp_height)

        stream_manager.play()
        time.sleep(1)

        action_manager.execute.assert_called_once()


if __name__ == '__main__':
    unittest.main()
