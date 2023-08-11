import cv2
import math
import functools


def get_cv_video_cap(video_src: str):
    return cv2.VideoCapture(video_src)


def get_duration_sec(cap):
    fps = get_fps(cap)
    frame_count = get_frame_count(cap)

    return math.floor(frame_count / fps)


def get_frame_dsize(cap):
    return (
        cap.get(cv2.CAP_PROP_FRAME_WIDTH),
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
    )


def get_frame_info(cap):
    return (
        cap.get(cv2.CAP_PROP_FRAME_WIDTH),
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
        cap.get(cv2.CAP_PROP_FPS),
        cap.get(cv2.CAP_PROP_FRAME_COUNT),
    )


def get_frame_count(cap):
    return cap.get(cv2.CAP_PROP_FRAME_COUNT)


def get_fps(cap):
    return cap.get(cv2.CAP_PROP_FPS)


def get_frame(t, cap):
    cap.set(cv2.CAP_PROP_POS_MSEC, t)
    res, img = cap.read()

    return res, img


def get_frame_as_cv_img(cap, t: int) -> cv2.Mat:
    res, img = get_frame(t, cap)
    return img


def get_frames_as_cv_img(cap, t_start_ms=0, t_end_ms=None, t_interval_ms=1000):
    result_res = []
    result_img = []

    if t_end_ms == None:
        t_end_ms = get_duration_sec(cap) * 1000

    for t in range(
        t_start_ms, t_end_ms, t_interval_ms
    ):  # range : use "<", not "<="
        res, img = get_frame(t * 1000, cap)
        # if res == False:
        #     raise ValueError("Failed to read frame.")
        result_res.append(res)
        result_img.append(img)

    return result_img


def get_video_frame_every_sec(cap, start_time_sec=0):
    media_time_sec = get_duration_sec(cap)
    result_res = []
    result_img = []

    for i in range(media_time_sec + 1):  # range : use "<", not "<="
        if i < start_time_sec:
            continue

        res, img = get_frame(i * 1000, cap)
        result_res.append(res)
        result_img.append(img)

    return result_res, result_img
