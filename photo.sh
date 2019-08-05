#!/bin/bash

FILENAME="photo-$(date "+%Y%m%d-%H%M%S").jpg"

raspistill -o "/home/pi/stills/remote/$FILENAME"

