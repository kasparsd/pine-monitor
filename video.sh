#!/bin/bash

FILENAME="video-$(date "+%Y%m%d-%H%M%S").h264"
FILEPATH="/home/pi/remote/videos/$FILENAME"

raspivid -w 1280 -h 720 -t 5000 -o "$FILEPATH"
MP4Box -add "$FILEPATH" "$FILEPATH.mp4"
rm "$FILEPATH"
