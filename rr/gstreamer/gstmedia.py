#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from gi.repository import Gst as gst
from gi.repository import GLib
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')


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
    CreateMedia(desc : str)
        Creates the media object from a string description

    DeleteMedia()
        Deletes the media object

    PlayMedia()
        Set the media state to playing

    StopMedia()
        Set the media state to stopped

    GetMedia()
        Getter for the private media object
    """

    def __init__(self):
        """
        Constructor for the Media Gstreamer Manager object
        """

        gst.init(None)

        self._pipeline = None

    def CreateMedia(self, desc):
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

    def DeleteMedia(self):
        """Deletes the media object
        """

        if self._pipeline is not None:
            del self._pipeline
            self._pipeline = None

    def PlayMedia(self):
        """Set the media state to playing

        Raises
        ------
        GstMediaError
            If couldn't set the media state to playing
        """

        try:
            ret = self._pipeline.set_state(gst.State.PLAYING)
            if gst.StateChangeReturn.FAILURE == ret:
                raise GstMediaError
        except GstMediaError as e:
            raise GstMediaError("Unable to play the media") from e

    def StopMedia(self):
        """Set the media state to stopped

        Raises
        ------
        GstMediaError
            If couldn't set the media state to stopped
        """

        try:
            ret = self._pipeline.set_state(gst.State.NULL)
            if gst.StateChangeReturn.FAILURE == ret:
                raise GstMediaError
        except GstMediaError as e:
            raise GstMediaError("Unable to stop the media") from e

    def GetMedia(self):
        """Getter for the private media object
        """
        return self._pipeline
