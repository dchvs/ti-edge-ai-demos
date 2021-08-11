#!/usr/bin/env python3

#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import time

from rr.display.display_manager import DisplayManager
from rr.gstreamer.imedia import IMedia
from rr.gstreamer.media_manager import MediaManager

#Use 8 or less, otherwise the display manager will throw an exception
NUM_STREAMS = 8
STREAM_NAME_PREFIX = "stream"

def main():
    print ("Display Manager Example Application")

    media_manager = MediaManager()
    display_manager = DisplayManager()

    for i in range(NUM_STREAMS):
        src = IMedia()
        src_name = STREAM_NAME_PREFIX + str(i)
        src_desc = "videotestsrc is-live=true ! video/x-raw,width=320,height=240 ! queue ! interpipesink async=false name=" + src_name 
        src.create_media(src_desc)
        media_manager.add_media(src_name, src)
        display_manager.add_stream(src_name)

    display_manager.create_display()
    media_manager.play_media()
    display_manager.play_display()

    input("Press Enter to close demo...")

    display_manager.stop_display()
    display_manager.delete_display()
    media_manager.stop_media()
        
if __name__ == "__main__":
    main()
