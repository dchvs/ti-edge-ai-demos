#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import gi  # nopep8
gi.require_version('Gst', '1.0')  # nopep8
gi.require_version('GLib', '2.0')  # nopep8
from gi.repository import Gst as gst  # nopep8
from gi.repository import GLib  # nopep8

import cv2
import numpy as np
import random
import unittest

from TI.postprocess import PostProcessDetection
from TI.preprocess import PreProcessDetection
from rr.ai.ai_manager import AIManager
from rr.ai.ai_manager import AIManagerError

model = "/opt/edge_ai_apps/models/detection/TFL-OD-200-ssd-mobV1-coco-mlperf-300x300/"
width = 1920
height = 1080
color = (100, 100, 100)
disp_width = 2040
disp_height = 1920


def get_media():
    return IMedia()


def create_img(width, height, rgb_color=(0, 0, 0)):
    img = np.zeros((height, width, 3), np.uint8)

    color = tuple(reversed(rgb_color))
    img[:] = color

    return img


class TestAIManager(unittest.TestCase):
    def setUp(self):
        global model, width, height, disp_width, disp_height

        self.model = model
        self.img = create_img(width, height, rgb_color=color)
        self.ai_manager = AIManager()

        self.disp_width = disp_width
        self.disp_height = disp_height

    def testnew_media(self):
        pass

    def testpreprocess_detection(self):
        img = self.ai_manager.preprocess_detection(self.img, self.model)
        self.assertTrue(0 != img.size)

    def testruntime(self):
        preprocess = PreProcessDetection(self.img, self.model)
        img = self.ai_manager.preprocess_detection(self.img, self.model)

        results = self.ai_manager.run_inference(img, self.model, preprocess)

    def testpostprocess(self):
        pass


class TestAIManagerFail(unittest.TestCase):
    def setUp(self):
        self.ai_manager = AIManager()

    def testnew_media(self):
        pass

    def testpreprocess(self):
        pass

    def testpostprocess(self):
        pass


if __name__ == '__main__':
    unittest.main()
