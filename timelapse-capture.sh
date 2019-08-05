#!/bin/bash

FILENAME="photo-$(date "+%Y%m%d-%H%M%S").jpg"
TIME=$(date +%H%M)

if [ "$TIME" -ge 600 -a "$TIME" -le 2100 ]; then
	raspistill -o "/home/pi/remote/timelapse/$FILENAME"
fi
