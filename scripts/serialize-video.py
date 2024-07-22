import json
import cv2
import numpy as np
import seaborn as sns
import sys
import time
import argparse

from lib import read_video, serialize_frame, compress_frame

parser = argparse.ArgumentParser(description="Print video to terminal")
parser.add_argument(
    "--file_path", type=str, required=True, help="Path to the video file"
)
parser.add_argument("--start_time", type=int, help="Start time in seconds")
parser.add_argument("--end_time", type=int, help="End time in seconds")
args = parser.parse_args()


target_width = 100
src_fps = 30
target_fps = 15


# Example usage
file_path = args.file_path
# get video duration
cap = cv2.VideoCapture(file_path)
src_fps = int(cap.get(cv2.CAP_PROP_FPS))

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / src_fps
cap.release()

start_time = 0  # Start time in seconds
end_time = duration  # End time in seconds

frames = read_video(file_path, start_time, end_time, target_width, target_fps)


# each frame is a 2D array, print it in terminal. if pixel is 0, use space, if pixel is 255, use '#'. refresh frame for every frame
# for idx, frame in enumerate(frames):
#     # print(idx, end="\r")
#     print(
#         "\n".join(
#             ["".join(["  " if pixel == 0 else "*" for pixel in row]) for row in frame]
#         ),
#         end="\r",
#     )
#     time.sleep(1 / target_fps)  # 30 fps
#     # run clear command in terminal to clear the screen
#     print("\033[H\033[J", end="\r")


with open("frames.json", "w") as f:
    json.dump([compress_frame(serialize_frame(frame)) for frame in frames], f)
