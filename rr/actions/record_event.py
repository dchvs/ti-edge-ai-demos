#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from threading import Timer

from rr.actions.gst_recording_media import GstRecordingMedia


class RecordEvent():
    def __init__(self, rec_dir):
        self._rec_dir = rec_dir
        self._medias_dict = {}

    def execute(self, media, image, rec_time, inf_filter):
        media_name = media.get_name()

        if media_name not in self._medias_dict:
            timestamp = image.get_timestamp()
            filename = self._rec_dir + "/" + "detection_recording_" + timestamp + ".ts"
            self._medias_dict[media_name] = {}
            self._medias_dict[media_name]['rec_media'] = GstRecordingMedia(
                filename)
            self._medias_dict[media_name]['recording'] = False
            self._medias_dict[media_name]['timer'] = None

        rec_media = self._medias_dict[media_name]['rec_media']
        rec_status = self._medias_dict[media_name]['recording']

        if not rec_status:
            self._start_recording(media_name, rec_time, inf_filter)
        else:
            self._start_timer(media_name, rec_time, inf_filter)

        # rec_media.push_image(image)

    def _start_timer(self, media_name, rec_time, inf_filter):
        media = self._medias_dict[media_name]

        if media['recording']:
            media['timer'].cancel()

        media['timer'] = Timer(rec_time, self._stop_recording, [media_name])

        inf_filter.set_enabled(True)
        media['timer'].start()

    def _start_recording(self, media_name, rec_time, inf_filter):
        self._start_timer(media_name, rec_time, inf_filter)
        self._medias_dict[media_name]['recording'] = True

    def _stop_recording(self, media_name):
        pass
