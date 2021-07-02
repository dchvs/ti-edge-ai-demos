#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import cv2
import logging


class ImageHandler:
    """
    Constructor to create an image handler
    Handles file operations over images
    """

    def loadImage(self, image_name):
        try:
            return cv2.imread(image_name)

        except Exception as e:
            logging.warning("Unable to load the image")

    def saveImage(self, image_name, img):
        try:
            cv2.imwrite(image_name, img)
        except Exception as e:
            logging.warning("Unable to save the image")

    def resizeImage(self, img, new_size):
        try:
            return cv2.resize(img, new_size, interpolation=cv2.INTER_LINEAR)

        except Exception as e:
            logging.warning("Unable to resize image")
