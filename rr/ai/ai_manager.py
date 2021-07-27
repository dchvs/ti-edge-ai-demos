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

    def __init__(self):
        """
        Constructor for the AI Manager object
        """

    def new_media(self, media):
        """Get a media input

        Parameters
        ----------
        media : media input
            The media received

        Raises
        ------
        AIManagerError
            If couldn't get the media
        """

    def preprocess_detection(self, media, model):
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

        preprocess = PreProcessDetection(media, model)
        img_preprocessed = preprocess.get_preprocessed_image(media)

        return img_preprocessed

    def run_inference(self, media, model):
        """Apply inference to the media

        Parameters
        ----------
        media : media input
            The media to preprocess

        inference_model : str
            The inference model to apply

        Raises
        ------
        AIManagerError
            If couldn't run the inference to the media
        """

        RunTime = eval(preprocess.params.run_time)
        run_time = RunTime(preprocess.params)
        results = run_time.run(img_preprocessed)

        return results

    def postprocess_detection(
            self,
            media,
            model,
            results,
            disp_width,
            disp_height):
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

        postprocess = PostProcessDetection(
            media, model, disp_width, disp_height)
        img_postprocessed = postprocess.get_postprocessed_image(media, results)

        return img_postprocessed
