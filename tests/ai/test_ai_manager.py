#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import cv2
import numpy as np
import random
import unittest
from unittest.mock import MagicMock

from TI.postprocess import PostProcessDetection
from TI.preprocess import PreProcessDetection
from rr.ai.ai_manager import AIManager
from rr.ai.ai_manager import AIManagerError
from rr.ai.ai_manager import AIManagerOnNewImage

model = "/opt/edge_ai_apps/models/detection/TFL-OD-200-ssd-mobV1-coco-mlperf-300x300/"
width = 1920
height = 1080
color = (100, 100, 100)
disp_width = 2040
disp_height = 1920


def create_img(width, height, rgb_color=(0, 0, 0)):
    img = np.zeros((height, width, 3), np.uint8)

    color = tuple(reversed(rgb_color))
    img[:] = color

    return img


def mock_img():
    global width, height, color

    return create_img(width, height, rgb_color=color)


def mock_on_new_prediction_cb(img, inference_results):
    global width, height, color

    return create_img(width, height, rgb_color=color)


def mock_on_new_postprocess_cb(img):
    pass


class TestAIManager(unittest.TestCase):
    def setUp(self):
        global model, width, height, disp_width, disp_height

        self.model = model
        self.img = create_img(width, height, rgb_color=color)
        self.ai_manager = AIManager(
            self.model,
            disp_width,
            disp_height,
            mock_on_new_prediction_cb,
            mock_on_new_postprocess_cb)

        self.disp_width = disp_width
        self.disp_height = disp_height

    def testpreprocess_detection(self):
        img = self.ai_manager.preprocess_detection(self.img)
        self.assertTrue(0 != img.size)

    def testruntime(self):
        preprocess = PreProcessDetection(self.model)
        img = self.ai_manager.preprocess_detection(self.img)

        results = self.ai_manager.run_inference(img)

    def testpostprocess_detection(self):
        preprocess = PreProcessDetection(self.model)
        img = self.ai_manager.preprocess_detection(self.img)
        results = self.ai_manager.run_inference(img)

        postprocess = PostProcessDetection(
            self.model, self.disp_width, self.disp_height)
        img = postprocess.get_postprocessed_image(self.img, results)
        self.assertTrue(0 != img.size)


class TestAIManagerOnNewImage(unittest.TestCase):
    def setUp(self):
        global model, width, height, disp_width, disp_height

        self.model = model
        self.disp_width = disp_width
        self.disp_height = disp_height

        self.img = mock_img()

        self.mock_on_new_prediction_cb = MagicMock()
        self.mock_on_new_postprocess_cb = MagicMock()

        self.ai_manager = AIManagerOnNewImage(
            model,
            disp_width,
            disp_height,
            self.mock_on_new_prediction_cb,
            self.mock_on_new_postprocess_cb)

    def testprocess_image(self):
        self.ai_manager.process_image(
            self.img, self.model, self.disp_width, self.disp_height)

        self.mock_on_new_prediction_cb.assert_called_once()
        self.mock_on_new_postprocess_cb.assert_called_once()


if __name__ == '__main__':
    unittest.main()
