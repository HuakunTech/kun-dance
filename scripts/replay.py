import sys
import time
import json
import argparse

from lib import decompress_frame, deserialize_frame

# read from ./frames.json and parse
with open("./frames.json", "r") as f:
    raw_frames = [decompress_frame(frame) for frame in json.load(f)]

fps = 15

# print to terminal
frames = []
for frame in raw_frames:
    frames.append(deserialize_frame(decompress_frame(frame)))


for idx, frame in enumerate(frames):
    # print(idx, end="\r")
    print(
        "\n".join(
            ["".join(["  " if pixel == 0 else "*" for pixel in row]) for row in frame]
        ),
        end="\r",
    )
    time.sleep(1 / fps)  # 30 fps
    # run clear command in terminal to clear the screen
    print("\033[H\033[J", end="\r")
