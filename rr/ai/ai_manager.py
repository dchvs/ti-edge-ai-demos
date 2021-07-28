#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import gi  # nopep8
gi.require_version('Gst', '1.0')  # nopep8
gi.require_version('GLib', '2.0')  # nopep8
from gi.repository import Gst as gst  # nopep8
from gi.repository import GLib  # nopep8

from TI.postprocess import PostProcessDetection
from TI.preprocess import PreProcessDetection
from TI.runtimes import *


class AIManagerError(RuntimeError):
    pass


class AIManager():
    """
    Class that handles the AI modules

    Attributes
    ----------

    Methods
    -------
    new_media(media : media input):
        Get a media input

    preprocess(media : media input, model : str)
        Preprocess the media

    run_inference(media : media input, model : str):
        Apply inference to the media

    postprocess(self, media, inference_model):
        Postprocess the media
    """

    def __init__(self, media, model, disp_width, disp_height):
        """
        Constructor for the AI Manager object
        """

        self.preprocess_obj = PreProcessDetection(model)

        RunTime = eval(self.preprocess_obj.params.run_time)
        self.inference_obj = RunTime(self.preprocess_obj.params)

        self.postprocess_obj = PostProcessDetection(
            model, disp_width, disp_height)

    def preprocess_detection(self, media):
        """Preprocess the media

        Parameters
        ----------
        media : media input
            The media to preprocess

        Raises
        ------
        AIManagerError
            If couldn't preprocess the media
        """

        img_preprocessed = self.preprocess_obj.get_preprocessed_image(media)

        return img_preprocessed

    def run_inference(self, media):
        """Apply inference to the media

        Parameters
        ----------
        media : media input
            The media to preprocess

        inference_model : str
            The inference model to apply

        preprocess : AI Preprocess object
            The AI Preprocess object

        Raises
        ------
        AIManagerError
            If couldn't run the inference to the media
        """

        results = self.inference_obj.run(media)

        return results

    def postprocess_detection(self, media, results):
        """Postprocess the media

        Parameters
        ----------
        media : media input
            The media to postprocess

        inference_model : str
            The inference model to apply

        Raises
        ------
        AIManagerError
            If couldn't postprocess the media
        """

        img_postprocessed = self.postprocess_obj.get_postprocessed_image(
            media, results)

        return img_postprocessed


class AIManagerOnNewImage(AIManager):
    """
    Class that performs the AI processing

    Attributes
    ----------

    Methods
    -------
    on_new_media(media : media input):
        Get a media input

    """

    def on_new_media(self, callback, model, disp_width, disp_height):
        """Get a media input

        Parameters
        ----------
        callback: function
            The callback function to receive the media

        Raises
        ------
        AIManagerError
            If couldn't get the media
        """

        media = callback()

        media_preprocessed = self.preprocess_detection(media)

        inference_results = self.run_inference(media_preprocessed)

        img_postprocessed = self.postprocess_detection(
            media, inference_results)

        return img_postprocessed
