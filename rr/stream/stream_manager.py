#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from rr.ai.ai_manager import AIManagerOnNewImage
from rr.gstreamer.media_manager import MediaManager


class OnNewImage():
    def __init__(self, ai_manager, model, disp_width, disp_height):
        self.ai_manager = ai_manager
        self.model = model
        self.disp_width = disp_width
        self.disp_height = disp_height

    def __call__(self, image):
        self.ai_manager.process_image(
            image, self.model, self.disp_width, self.disp_height)


class StreamManagerError(RuntimeError):
    pass


class StreamManager():
    """
    Class that orchestrates the stream interoperations

    Attributes
    ----------

    Methods
    -------
    """

    def __init__(
            self,
            ai_manager,
            media_manager,
            model,
            disp_width,
            disp_height):
        """
        Constructor for the Stream Manager object
        """

        self.ai_manager = ai_manager
        self.media_manager = media_manager

        cb = OnNewImage(ai_manager, model, disp_width, disp_height)
        self.media_manager.install_callback(cb)

    def play(self):
        """
        Start the stream server
        """

        try:
            self.media_manager.play_media()
        except MediaManagerError as e:
            raise StreamManagerError("Unable to play the stream") from e
