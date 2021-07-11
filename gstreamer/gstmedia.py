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
        gst.init(None)

        self._pipeline = None

    def CreateMedia(self, desc):
        try:
            self._pipeline = gst.parse_launch(desc)
        except ValueError as e:
            logging.error("Unable to create the media")
            return False

        return True

    def DeleteMedia(self):
        if self._pipeline is not None:
            del self._pipeline
            self._pipeline = None

        return True

    def PlayMedia(self):
        try:
            self._pipeline.set_state(gst.State.PLAYING)
        except ValueError as e:
            logging.error("Unable to play the media")

    def StopMedia(self):
        try:
            self._pipeline.set_state(gst.State.NULL)
        except ValueError as e:
            logging.error("Unable to stop the media")

    def GetMedia(self):
        return self._pipeline
