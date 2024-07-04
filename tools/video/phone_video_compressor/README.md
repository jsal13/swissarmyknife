# Phone Video Compressor

## Last Updated

2024-07-04

## Status

**Working.**

## Description

Given a phone video, this tool creates a new copy which resizes the video to 720p and compresses it.  Depending on the video, this can be a significant amount of compression with no noticable effects.  My Pixel 6 videos compress to around 10% of their original size.

Saves this compressed copy in a `/compressed` subfolder of the original file's directory.

## Quickstart

To compress a video file:

```bash
# With Python:
python ./compressor.py /path/to/the/mp4/example.mp4

# With `just` from this folder root.  Uses docker:
just compress-video /path/to/the/mp4s/example.mp4
```
