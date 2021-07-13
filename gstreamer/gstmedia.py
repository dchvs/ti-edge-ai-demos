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
    Class that creates the GStreamer handler
    """

    def __init__(self):
        """
        Constructor for the Media Gstreamer Manager object

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
            Set the media state to stop

        GetMedia()
            Getter for the private media object
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
        GLib.GError, ValueError
            If the description fails to create the media
        """

        try:
            self._pipeline = gst.parse_launch(desc)
        except ValueError as e:
            logging.error("Unable to create the media")
            return False

        return True

    def DeleteMedia(self):
        """Deletes the media object
        """

        if self._pipeline is not None:
            del self._pipeline
            self._pipeline = None

        return True

    def PlayMedia(self):
        """Set the media state to playing

        Raises
        ------
        GLib.GError, ValueError
            If couldn't set the media state to playing
        """

        try:
            self._pipeline.set_state(gst.State.PLAYING)
        except ValueError as e:
            logging.error("Unable to play the media")
            return False

        return True

    def StopMedia(self):
        """Set the media state to stop

        Raises
        ------
        GLib.GError, ValueError
            If couldn't set the media state to stop
        """

        try:
            self._pipeline.set_state(gst.State.NULL)
        except ValueError as e:
            logging.error("Unable to stop the media")
            return False

        return True

    def GetMedia(self):
        """Getter for the private media object
        """
        return self._pipeline
