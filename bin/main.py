#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from utils.imagehandler import *
from TI.postprocess import *
from TI.preprocess import *
from TI.runtimes import *

model_dir = "/opt/edge_ai_apps/models/detection/TFL-OD-200-ssd-mobV1-coco-mlperf-300x300/"
input_image = "data/0004.jpg"
output_image = "result.jpg"
(disp_width, disp_height) = (1280, 720)


def main():
    image_handler = ImageHandler()
    img = image_handler.loadImage(input_image)

    # Preprocess
    preprocess = PreProcessDetection(img, model_dir)
    img_preprocessed = preprocess.get_preprocessed_image(img)

    # Inference
    RunTime = eval(preprocess.params.run_time)
    run_time = RunTime(preprocess.params)
    results = run_time.run(img_preprocessed)

    # Postprocess
    postprocess = PostProcessDetection(
        img, model_dir, *(disp_width, disp_height))
    img = postprocess.get_postprocessed_image(img, results)

    image_handler.saveImage(output_image, img)


if __name__ == "__main__":
    main()
