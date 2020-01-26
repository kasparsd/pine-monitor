#!/bin/sh

# Rotate 15 deg clockwise, crop to 2924x1644, offset left 436, top 736
# drawtext=text='%{localtime\:%T}':x=60:y=60:fontsize=36:fontcolor=white

cat $(find ./timelapse/* -mtime -7) | \
	ffmpeg -y -f image2pipe -i - \
	-r 30 -q 1 -vf "rotate=15*PI/180,crop=2924:1644:218:368" \
	tl.mp4
