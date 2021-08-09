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

from rr.gstreamer.gstmedia import GstMedia


class GstRecordingMedia(GstMedia):
    def __init__(self):
        super().__init__()

        desc = "appsrc name=src ! x264enc ! h264parse ! mpegtsmux ! filesink location=/tmp/file.ts name=sink"
        self.create_media(desc)
        self._appsrc = self._pipeline.get_by_name('src')
        self._filesink = self._pipeline.get_by_name('sink')


def push_image(self, image):
    buffer = image.get_buffer()
    GstVideo.buffer_add_video_meta(
        buffer,
        0,
        image.get_format(),
        image.get_width(),
        image.get_height())
    self._appsrc.emit("push-buffer", buffer)
