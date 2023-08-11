import cv2
import base64
import numpy as np


def __clamp(min_value, value, max_value):
    return min(max(min_value, value), max_value)


def imcrop_around_square(src_cv_img: cv2.Mat, pt1: list[int], pt2: list[int]):
    width, height = src_cv_img.shape[1], src_cv_img.shape[0]
    x1 = int(__clamp(0, pt1[0], width))
    y1 = int(__clamp(0, pt1[1], height))

    x2 = int(__clamp(0, pt2[0], width))
    y2 = int(__clamp(0, pt2[1], height))

    return src_cv_img.copy()[y1:y2, x1:x2]  # 画像1から切り抜く


def cvt_to_dataurl(cv_img, ext="png"):
    retval, buffer = cv2.imencode(f".png", cv_img)
    data = base64.b64encode(buffer).decode("utf-8")
    return f"data:image/{ext};base64,{data}"


def bgr_to_bin(cv_img, threshold=150, maxval=255):
    grayscale = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    _, im_bin = cv2.threshold(grayscale, threshold, maxval, cv2.THRESH_BINARY)
    return im_bin


def compare_hists(cv_img_1: cv2.Mat, cv_img_2: cv2.Mat, calc_hist_method=0):
    assert cv_img_1.shape == cv_img_2.shape  # assert if dim is equal

    ndim = cv_img_1.shape[2] if len(cv_img_1.shape) == 3 else 1
    hist_img1 = []
    hist_img2 = []

    for i in range(ndim):
        hist_img1.append(cv2.calcHist([cv_img_1], [i], None, [256], [0, 256]))
        hist_img2.append(cv2.calcHist([cv_img_2], [i], None, [256], [0, 256]))

    return [
        cv2.compareHist(hist_img1[i], hist_img2[i], calc_hist_method)
        for i in range(ndim)
    ]


def calc_vh_projection_profile_corr(
    cvimg_bgr_prevframe,
    cvimg_bgr_currframe,
    th_corr_diff=0.7,
    th_img_binarization=150,
):
    (
        h_profile_prevframe,
        v_profile_prevframe,
    ) = calc_projection_profile(cvimg_bgr_prevframe, th_img_binarization)

    (
        h_profile_currframe,
        v_profile_currframe,
    ) = calc_projection_profile(cvimg_bgr_currframe, th_img_binarization)

    v_corr = np.corrcoef(h_profile_prevframe, h_profile_currframe)[0, 1]
    h_corr = np.corrcoef(v_profile_prevframe, v_profile_currframe)[0, 1]

    return h_corr, v_corr


def calc_projection_profile(
    cv_bgr_img: cv2.Mat,
    th_img_binarization=100,
):
    cv_gray_img = cv2.cvtColor(cv_bgr_img, cv2.COLOR_BGR2GRAY)
    _, cv_bin_img = cv2.threshold(
        cv_gray_img, th_img_binarization, 255, cv2.THRESH_BINARY
    )
    cv_bin_img[cv_bin_img == 0] = 1
    cv_bin_img[cv_bin_img == 255] = 0

    # img1に関する投影プロジェクションの計算
    horizontal_profile = np.sum(cv_bin_img, axis=1)
    vertical_profile = np.sum(cv_bin_img, axis=0)

    return (horizontal_profile, vertical_profile)
