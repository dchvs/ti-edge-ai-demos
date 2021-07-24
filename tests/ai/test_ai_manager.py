#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import gi  # nopep8
gi.require_version('Gst', '1.0')  # nopep8
gi.require_version('GLib', '2.0')  # nopep8
from gi.repository import Gst as gst  # nopep8
from gi.repository import GLib  # nopep8

import random
import unittest

from rr.gstreamer.ai_manager import AIManager
from rr.gstreamer.ai_manager import AIManagerError


def get_media():
    return IMedia()


class TestAIManager(unittest.TestCase):
    def setUp(self):
        self.ai_manager = AIManager()

    def testnew_media(self):

    def testpreprocess(self):

    def testpostprocess(self):


class TestAIManagerFail(unittest.TestCase):
    def setUp(self):
        self.ai_manager = AIManager()

    def testnew_media(self):

    def testpreprocess(self):

    def testpostprocess(self):


if __name__ == '__main__':
    unittest.main()
