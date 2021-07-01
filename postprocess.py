#!/usr/bin/env python3

#  Copyright (C) 2021 Texas Instruments Incorporated - http://www.ti.com/
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#    Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#    Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
#
#    Neither the name of Texas Instruments Incorporated nor the names of
#    its contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import cv2
import numpy as np

from getconfig import *
from classnames import *


class PostProcess:
    def __init__(self, img, model_dir, disp_width, disp_height):
        # Get parsed the model params
        config = GetConfigYaml(model_dir)
        self.params = config.params

        # Get the image
        self.img = img

        # Get the model and demo names
        self.model_name = model_dir[:len(model_dir) - 1]
        self.demo_name = 'Simple example'

        # Get the output display window size
        self.disp_width = disp_width
        self.disp_height = disp_height

        # Get the image size
        (img_height, img_width, img_channels) = img.shape
        self.img_height = img_height
        self.img_width = img_width
        self.img_channels = img_channels

    def overlay_title(self, img, padx, pady):
        padx_2 = int(padx / 2)
        pady_2 = int(pady / 2)

        img = cv2.copyMakeBorder(img,
                                 pady_2,
                                 pady - pady_2,
                                 padx_2,
                                 padx - padx_2,
                                 cv2.BORDER_CONSTANT)

        img = cv2.putText(img, "Texas Instruments - Edge Analytics", (40, 40),
                          cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

        img = cv2.putText(img, self.demo_name, (40, 40 + 50),
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        img = cv2.putText(img, "model : " + self.model_name, (40, 40 + 100),
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return img


class PostProcessDetection(PostProcess):
    def overlay_bounding_box(self, frame, results, classnames, score_thresh,
                             scalex, scaley, label_offset, formatter):
        class_IDs, scores, bounding_boxes = results
        for i, score in enumerate(np.squeeze(scores, axis=0)):
            if (score <= score_thresh):
                continue
            box = bounding_boxes[0][i]
            box = [int(box[formatter.index(0)] * scalex),
                   int(box[formatter.index(1)] * scaley),
                   int(box[formatter.index(2)] * scalex),
                   int(box[formatter.index(3)] * scaley)]
            class_id = label_offset[int(class_IDs[0][i])]
            box_color = (int(120 * score), int(120 * score), int(50 * score))
            text_color = (int(240 * score), int(240 * score), int(240 * score))
            cv2.rectangle(frame, (box[0], box[1]),
                          (box[2], box[3]), box_color, 2)
            cv2.rectangle(frame,
                          (int((box[2] + box[0]) / 2) - 5,
                           int((box[3] + box[1]) / 2) + 5),
                          (int((box[2] + box[0]) / 2) + 160,
                              int((box[3] + box[1]) / 2) - 15),
                          box_color,
                          -1)
            cv2.putText(frame,
                        classnames[class_id],
                        (int((box[2] + box[0]) / 2),
                         int((box[3] + box[1]) / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        text_color)

        return frame

    def get_postprocessed_image(self, img, results):
        classnames = eval(self.params.dataset)
        scalex = self.img_width / self.params.resize[0]
        scaley = self.img_height / self.params.resize[1]
        threshold = 0.5

        img = self.overlay_bounding_box(
            img,
            results,
            classnames,
            threshold,
            scalex,
            scaley,
            self.params.label_offset,
            self.params.formatter)

        img = self.overlay_title(img, self.disp_width - self.img_width,
                                 self.disp_height - self.img_height)

        return img


class PostProcessClassification(PostProcess):
    def overlay_top5_classnames(
            self,
            frame,
            results,
            classnames,
            label_offset):
        """
        Process the results of the image classification model and draw text
        describing top 5 detected objects on the image.

        Args:
            frame (numpy array): Input image in BGR format where the overlay should
        be drawn
        results (numpy array): Output of the model run
            classnames (dictionary): Map for class ID to class name
        """
        top5 = np.argpartition(results[0], -5)[0][:-6:-1]
        orig_width = frame.shape[1]
        orig_height = frame.shape[0]
        # cv2.rectangle(frame, (0, 0), (int(orig_width/4), int(orig_height/4)), \
        #                               (40, 40, 40), -1)
        cv2.putText(frame, "Top 5 detected classes:", (int(
            3 * orig_width / 4), 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        row = 1
        for idx in top5:
            cv2.putText(
                frame,
                "%s" %
                classnames.get(
                    idx +
                    label_offset),
                (int(
                    3 *
                    orig_width /
                    4),
                    40 +
                    40 *
                    row),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,
                 255,
                 255),
                2)
            row = row + 1

        end = time()
        return frame

    def get_postprocessed_image(self, img):
        classnames = eval(self.params.dataset)

        img = overlay_title(
            img,
            self.disp_width -
            self.img_width,
            self.disp_height -
            self.img_height)
        img = overlay_top5_classnames(
            img, results, classnames, self.params.label_offset)
