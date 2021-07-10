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
    Class that creates the GStreamer handler
    """

    def __init__(self):
        # Init the gst
        gst.init(None)

        self.pipeline = None

    def CreatePipeline(self, desc):
        try:
            self.pipeline = gst.parse_launch(desc)
        except ValueError as e:
            logging.error("Unable to create the pipeline")

        return True

    def DeletePipeline(self):
        if self.pipeline is not None:
            del self.pipeline
            self.pipeline = None

        return True

    def PlayPipeline(self):
        try:
            self.pipeline.set_state(gst.State.PLAYING)
        except ValueError as e:
            logging.error("Unable to play the pipeline")

    def StopPipeline(self):
        try:
            self.pipeline.set_state(gst.State.NULL)
        except ValueError as e:
            logging.error("Unable to stop the pipeline")
