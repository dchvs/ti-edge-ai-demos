#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import gi  # nopep8
gi.require_version('Gst', '1.0')  # nopep8
gi.require_version('GLib', '2.0')  # nopep8
from gi.repository import Gst as gst  # nopep8
from gi.repository import GLib  # nopep8


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
        self.callback_sample = None

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
        if gst.StateChangeReturn.FAILURE == ret:
            raise GstMediaError("Unable to play the media")

        # Install the buffer callback that passes the image media to a client
        if self.callback is not None:
            self.install_buffer_callback()

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

    def install_callbacks(self, callback, callback_sample):
        if callback is None:
            raise GstMediaError("Invalid callback")

        self.callback = callback

        self.callback_sample = callback_sample

    def install_buffer_callback(self):
        try:
            appsink = self._pipeline.get_by_name("appsink")
            appsink.connect("new-sample", self._on_new_buffer, appsink)

        except AttributeError as e:
            raise GstMediaError("Unable to install buffer callback") from e

    def _on_new_buffer(self, appsink, data):
        sample = appsink.emit("pull-sample")

        buf = sample.get_buffer()

        gst_memory = buf.get_all_memory()
        ret, minfo = gst_memory.map(gst.MapFlags.READ)

        if minfo.data is None:
            return gst.FlowReturn.ERROR

        self.callback(minfo.data)

        gst_memory.unmap(minfo)

        # Callback the GstSample object to other process
        if callback_sample is not None:
            self.callback_sample(sample)

        return gst.FlowReturn.OK

    def get_media(self):
        """Getter for the private media object
        """
        return self._pipeline


class GstSample():
    def __init__(self):
        self.sample = None
        self.map_flags = gst.MapFlags.READ or gst.MapFlags.WRITE
        self.gst_memory_obj = None

    def add_gst_sample(self, sample):
        self.sample = sample

    def get_shape_from_caps(self):
        caps = self.sample.get_caps()
        h, w, format = (caps.get_structure(0).get_value("height"),
                        caps.get_structure(0).get_value("width"),
                        caps.get_structure(0).get_value("format")
                        )

        return h, w, format

    def map_buffer(self):
        buf = self.sample.get_buffer()
        self.gst_memory_obj = buf.get_all_memory()

        ret, minfo = self.gst_memory_obj.map(self.map_flags)
        if ret is None:
            return ret

        return minfo

    def unmap_buffer(self, minfo):
        self.gst_memory_obj.unmap(minfo)
