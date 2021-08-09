#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import numpy as np
import time

import gi  # nopep8
gi.require_version('Gst', '1.0')  # nopep8
gi.require_version('GLib', '2.0')  # nopep8
from gi.repository import Gst as gst  # nopep8
from gi.repository import GLib  # nopep8


def construct_image_from_gst_sample(sample):
    buf = sample.get_buffer()
    caps = sample.get_caps()

    shape_ = (caps.get_structure(0).get_value("height"),
              caps.get_structure(0).get_value("width"),
              # Switch this value according to the caps format
              3)

    image_array = np.ndarray(
        shape=shape_,
        dtype=np.uint8,
        buffer=buf.extract_dup(
            0,
            buf.get_size()))

    return image_array


class GstMediaError(RuntimeError):
    pass


class GstMedia():
    """
    Class that creates the GStreamer handler

    Attributes
    ----------
    _pipeline : GstElement
        A private GStreamer pipeline object

    Methods
    -------
    create_media(desc : str)
        Creates the media object from a string description

    delete_media()
        Deletes the media object

    play_media()
        Set the media state to playing

    stop_media()
        Set the media state to stopped

    get_media()
        Getter for the private media object
    """

    def __init__(self):
        """
        Constructor for the Media Gstreamer Manager object
        """

        gst.init(None)

        self._pipeline = None
        self.callback = None

    def create_media(self, desc):
        """Creates the media object from a string description

        Parameters
        ----------
        desc : str
            The media description to create

        Raises
        ------
        GstMediaError
            If the description fails to create the media
        """

        try:
            self._pipeline = gst.parse_launch(desc)
        except GLib.GError as e:
            raise GstMediaError("Unable to create the media") from e

    def delete_media(self):
        """Deletes the media object
        """

        if self._pipeline is not None:
            del self._pipeline
            self._pipeline = None

    def play_media(self):
        """Set the media state to playing

        Raises
        ------
        GstMediaError
            If couldn't set the media state to playing
        """

        ret = self._pipeline.set_state(gst.State.PLAYING)
        if gst.StateChangeReturn.SUCCESS != ret:
            raise GstMediaError("Unable to play the media")

        # Send the buffer images to the installed callback
        self.on_new_buffer()

    def stop_media(self):
        """Set the media state to stopped

        Raises
        ------
        GstMediaError
            If couldn't set the media state to stopped
        """

        ret = self._pipeline.set_state(gst.State.NULL)
        if gst.StateChangeReturn.FAILURE == ret:
            raise GstMediaError("Unable to stop the media")

    def install_callback(self, callback):
        if callback is None:
            raise GstMediaError("Invalid callback")

        self.callback = callback

    def on_new_buffer(self):
        try:
            appsink = self._pipeline.get_by_name("appsink")
            appsink.connect("new-sample", self._on_new_buffer, appsink)
            time.sleep(1)
        except AttributeError as e:
            raise GstMediaError("Unable to get sample from buffer") from e

    def _on_new_buffer(self, appsink, data):
        sample = appsink.emit("pull-sample")

        image_array = construct_image_from_gst_sample(sample)
        if image_array is None:
            return gst.FlowReturn.ERROR

        self.callback(image_array)

        return gst.FlowReturn.OK

    def get_media(self):
        """Getter for the private media object
        """
        return self._pipeline
