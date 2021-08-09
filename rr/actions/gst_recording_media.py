#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import gi  # nopep8
gi.require_version('Gst', '1.0')  # nopep8
gi.require_version('GLib', '2.0')  # nopep8
gi.require_version('GstVideo', '1.0')  # nopep8
from gi.repository import GstVideo
from gi.repository import Gst
from gi.repository import GLib

from rr.gstreamer.gst_media import GstMedia


class GstRecordingMedia(GstMedia):
    def __init__(self):
        super().__init__()

    def _init_pipe(self, image):
        desc = "appsrc name=src ! video/x-raw,width=%d,height=%d,format=%s,framerate=30/1 ! videoconvert ! x264enc speed-preset=ultrafast tune=zerolatency ! h264parse ! mpegtsmux ! filesink location=/tmp/file.ts name=sink" % (
            image.get_width(), image.get_height(), GstVideo.VideoFormat.to_string(image.get_format()))
        self.create_media(desc)
        self._appsrc = self._pipeline.get_by_name('src')
        self._filesink = self._pipeline.get_by_name('sink')

        self.play_media()

    def push_image(self, image):
        if self._pipeline is None:
            self._init_pipe(image)
        buffer = image.get_buffer()
        self._appsrc.emit("push-buffer", buffer)

    def __del__(self):
        self.delete_media()
