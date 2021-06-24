#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>
#
#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

from imagehandler import *
from preprocess import *
from postprocess import *
from runtimes import *

from classnames import *

model_dir = "/opt/edge_ai_apps/models/detection/TFL-OD-200-ssd-mobV1-coco-mlperf-300x300/"

#params = utils.Params(args.model)

(cam_width, cam_height) = (425, 326)
(disp_width, disp_height) = (640, 420)
#(cam_width, cam_height) = (1280, 720)
#(disp_width, disp_height) = (5000, 3020)


def main():
    #    global classnames
    image_handler = ImageHandler()
    img = image_handler.loadImage("0004.jpg")
    img_orig = image_handler.loadImage("0004.jpg")

    preprocess = PreProcessDetection(img_orig, model_dir)
    img_pre = preprocess.get_preprocessed_image(img_orig)

    postprocess = PostProcessDetection(img_orig, model_dir)

    RunTime = eval(postprocess.params.run_time)
    run_time = RunTime(postprocess.params)
    results = run_time.run(img_pre)

    classnames = eval(postprocess.params.dataset)
    scalex = cam_width / postprocess.params.resize[0]
    scaley = cam_height / postprocess.params.resize[1]

    print ("scalex = %d " % (scalex))
    print ("scaley = %d " % (scaley))

    img_orig = postprocess.get_postprocessed_image(
        img_orig, results, classnames, scalex, scaley)

    image_handler.saveImage("falcon_postprocess.jpg", img_orig)


if __name__ == "__main__":
    main()
