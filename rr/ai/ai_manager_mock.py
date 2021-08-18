#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from bin.utils.imagehandler import ImageHandler
from rr.gstreamer.gst_media import GstImage
from rr.gstreamer.gst_media import GstUtils


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

        return image

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

        classID = (array([[15., 15., 15., 15., 15., 15., 15., 15., 15., 15., 15.]],
                         dtype=float32)

                   scores=array([[0.9819941, 0.97701955, 0.43781853, 0.43781853, 0.43781853,
                                  0.377575, 0.377575, 0.3208106, 0.3208106, 0.3208106,
                                  0.3208106]], dtype=float32)

                   bbox=array([[[41.319145, 210.90213, 242.32146, 299.09787],
                                [38.450996, 7.6868715, 300.02994, 180.86444],
                                [47.47543, 59.681156, 234.6865, 182.08157],
                                [87.04913, 201.42395, 293.9264, 299.16367],
                                [122.66138, 24.483088, 296.35184, 166.69206],
                                [74.31985, 89.84922, 301.43396, 178.29462],
                                [177.2659, 97.23523, 285.284, 279.82693],
                                [100.98614, 243.40727, 277.87695, 293.18192],
                                [47.48902, 183.54085, 212.71059, 291.55896],
                                [91.473526, 95.46426, 260.8768, 237.67322],
                                [116.78903, 210.84447, 270.07352, 286.9936]]],
                              dtype=float32))

        return classID, scores, bbox

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

        return image


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
            disp_height):

        super().__init__(model, disp_width, disp_height)

        self.on_new_prediction_cb_ = None

    def install_callback(self, on_new_prediction_cb_):
        self.on_new_prediction_cb_ = on_new_prediction_cb_

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

        gst_media = image.get_media()

        img = ImageHandler.buffer_to_np_array(
            image.get_data(), image.get_width(), image.get_height())

        image_preprocessed = self.preprocess_detection(img)

#        inference_results = self.run_inference(image_preprocessed)

#        image_postprocessed = self.postprocess_detection(
#            img, inference_results)

        image_postprocessed = img
        # Create GstBuffer from postprocess image
        h, w, c = image_postprocessed.shape
        size = h * w * c
        buffer = GstUtils.buffer_new_wrapped_full(
            image_postprocessed.tobytes(), size)

        # Create GstImage
        sample = image.get_sample()
        caps = sample.get_caps()
        sample2 = GstUtils.sample_new(buffer, caps)
        fmt = 'RGB'
        image2 = GstImage(w, h, fmt, sample2, image.get_media())

        self.on_new_prediction_cb_(
            inference_results,
            image,
            gst_media)
