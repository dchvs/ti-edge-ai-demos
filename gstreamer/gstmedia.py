#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from gi.repository import Gst as gst
from gi.repository import GLib
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')


class GstMedia():
    """
    Constructor for the Media Gstreamer Manager object
    Class that creates the Gstreamer handler
    """

    def __init__(self):
        # Init the gst
        gst.init(None)

        self.pipeline = None

    def CreatePipeline(self, desc):
        self.pipeline = gst.parse_launch(desc)

        if self.pipeline is None:
            return False

        return True

    def DeletePipeline(self):
        del self.pipeline

        return True

    def PlayPipeline(self):
        self.pipeline.set_state(gst.State.PLAYING)

    def StopPipeline(self):
        self.pipeline.set_state(gst.State.NULL)
