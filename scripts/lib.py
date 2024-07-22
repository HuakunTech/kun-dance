import cv2
import numpy as np


def serialize_frame(frame: np.ndarray) -> str:
    # convert 2D array to a single string. 0 is space, 255 is '#'. each line joined with '\n'
    return "\n".join(
        ["".join(["o" if pixel == 0 else "l" for pixel in row]) for row in frame]
    )


def deserialize_frame(frame_str: str) -> np.ndarray:
    # convert string to 2D array. "o" is 0, "l" is 255. each line is separated by '\n'
    return np.array(
        [[0 if char == "o" else 255 for char in row] for row in frame_str.split("\n")]
    )


def compress_frame(frame_str: str) -> str:
    """Each char can be "o" or "l". compress consecutive same char to a number followed by the char."""
    compressed = []
    count = 1
    prev_char = frame_str[0]
    for char in frame_str[1:]:
        if char == prev_char:
            count += 1
        else:
            if count > 1:
                compressed.append(str(count) + prev_char)
            else:
                compressed.append(prev_char)
            count = 1
            prev_char = char
    compressed.append(str(count) + prev_char)
    return "".join(compressed)


def decompress_frame(compressed_frame: str) -> str:
    """Each char can be "o" or "l". compress consecutive same char to a number followed by the char."""
    decompressed = []
    count = ""
    for char in compressed_frame:
        if char.isdigit():
            count += char
        else:
            if count:
                decompressed.append(int(count) * char)
                count = ""
            else:
                decompressed.append(char)
    return "".join(decompressed)
    # return np.array(decompressed)


def read_video(
    file_path: str, start_time: int, end_time: int, target_width: int, target_fps: int
) -> list[np.ndarray]:
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return []

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    # Convert start and end time to frame indices
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Check if start and end times are within the video duration
    if start_frame > total_frames or end_frame > total_frames:
        print("Error: Start or end time is beyond the video duration.")
        return []

    # Set the current frame position to the start frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frames = []
    current_frame = start_frame
    while cap.isOpened() and current_frame <= end_frame:
        ret, frame = cap.read()
        if not ret:
            break

        # convert frame to grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        width = frame.shape[1]
        # crop the frame in x direction, only keep the center 50%
        frame = frame[:, width // 5 : width * 4 // 5]
        # sample frame
        sample_rate = width // target_width
        frame = frame[::sample_rate, ::sample_rate]
        frame[frame < 30] = 0
        frame[frame >= 30] = 255
        # Append the frame as a numpy array (vector) to the list
        frames.append(frame)

        current_frame += 1

    frame_sample_rate = int(fps / target_fps)
    frames = frames[::frame_sample_rate]
    # Release the video capture object
    cap.release()
    return frames
