#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from threading import Lock

from bin.utils.imagehandler import ImageHandler
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
    preprocess_obj : PreProcessDetection object
        The PreProcessDetection object

    preprocess_obj : PreProcessDetection object
        The PreProcessDetection object

    Methods
    -------
    preprocess_detection(image : image input)
        Preprocess the image according to the model

    run_inference(image : image input):
        Apply inference to the image

    postprocess_detection(image : image input, results : run_inference return):
        Postprocess the image according to the inference results
    """

    def __init__(
            self,
            model,
            disp_width,
            disp_height):
        """
        Constructor for the AI Manager object
        """

        self.preprocess_obj = PreProcessDetection(model)

        RunTime = eval(self.preprocess_obj.params.run_time)
        self.inference_obj = RunTime(self.preprocess_obj.params)

        self.postprocess_obj = PostProcessDetection(
            model, disp_width, disp_height)

    def preprocess_detection(self, image):
        """Preprocess the image

        Parameters
        ----------
        image : image input
            The image to preprocess

        Raises
        ------
        AIManagerError
            If couldn't preprocess the image
        """

        img_preprocessed = self.preprocess_obj.get_preprocessed_image(image)

        return img_preprocessed

    def run_inference(self, image):
        """Apply inference to the image

        Parameters
        ----------
        image : image input
            The image to preprocess

        inference_model : str
            The inference model to apply

        preprocess : AI Preprocess object
            The AI Preprocess object

        Raises
        ------
        AIManagerError
            If couldn't run the inference to the image
        """

        results = self.inference_obj.run(image)

        return results

    def postprocess_detection(self, image, results):
        """Postprocess the image

        Parameters
        ----------
        image : image input
            The image to postprocess

        inference_model : str
            The inference model to apply

        Raises
        ------
        AIManagerError
            If couldn't postprocess the image
        """

        img_postprocessed = self.postprocess_obj.get_postprocessed_image(
            image, results)

        return img_postprocessed


class AIManagerOnNewImage(AIManager):
    """
    Class that performs the AI processing

    Attributes
    ----------

    Methods
    -------

    """

    def __init__(
            self,
            model,
            disp_width,
            disp_height,
            on_new_prediction_cb,
            on_new_postprocess_cb):

        super().__init__(model, disp_width, disp_height)

        self.on_new_prediction_cb = on_new_prediction_cb
        self.on_new_postprocess_cb = on_new_postprocess_cb

        self.on_new_prediction_cb_ = None

        self._on_new_prediction_mutex = Lock()

    def install_callback(self, on_new_prediction_cb_):
        self._on_new_prediction_mutex.acquire()
        self.on_new_prediction_cb_ = on_new_prediction_cb_
        self._on_new_prediction_mutex.release()

    def process_image(self, image, model, disp_width, disp_height):
        """Get a image input

        Parameters
        ----------
        callback: function
            The callback function to receive the image

        Raises
        ------
        AIManagerError
            If couldn't get the image
        """

        gst_media = image.get_gst_media_obj()

        img = ImageHandler.buffer_to_np_array(
            image.get_data(), image.get_width(), image.get_height())

        image_preprocessed = self.preprocess_detection(img)

        inference_results = self.run_inference(image_preprocessed)

        self.on_new_prediction_cb(image_preprocessed, inference_results)

        image_postprocessed = self.postprocess_detection(
            img, inference_results)

        self.on_new_postprocess_cb(image_preprocessed)

        self._on_new_prediction_mutex.acquire()
        self.on_new_prediction_cb_(
            inference_results,
            image_postprocessed,
            gst_media)

        self._on_new_prediction_mutex.release()
