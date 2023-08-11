import cv2
import os
import time
from datetime import datetime
import json
from pathlib import Path
from functools import cache
from skimage.metrics import (
    structural_similarity as compute_ssim,
    mean_squared_error as compute_mse,
    peak_signal_noise_ratio as compute_psnr,
)
import util.paths as paths
import util.video as vutil
from util.asset import AssetId, get_asset_id
import util.cvimg as cvimutil
import util.plot as pltutil


# 関数の実行時間を計測するデコレータ
def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time of {func.__name__}: {execution_time} seconds")
        return result

    return wrapper


@cache
def get_video_frames(path: str):
    cap = vutil.get_cv_video_cap(path)
    frames = vutil.get_frames_as_cv_img(cap)

    return frames, cap


@measure_time
def main(asset_id: str, resize_dsize=None):
    print(asset_id)
    cap = vutil.get_cv_video_cap(paths.path_file_video(asset_id))

    document_scroll_tl = None
    with open(paths.path_file_scroll_tl(asset_id), "r") as fp:
        document_scroll_tl = json.load(fp)["tl_document_scrollY"]

    document_cv_img = cv2.imread(paths.path_file_document_concat_img(asset_id))
    print(f"document img shape: {document_cv_img.shape}")

    result = []

    for section in document_scroll_tl:
        if section[1] == None:
            continue

        t = section[0]
        match_result_viewport = section[-1]

        print(f"Analyzing frame t = {t}")

        im_frame = vutil.get_frame_as_cv_img(cap, t * 1000)

        if resize_dsize != None:
            im_frame = cv2.resize(im_frame, resize_dsize)

        frame_dsize = im_frame.shape[1], im_frame.shape[0]

        im_matched = cvimutil.imcrop_around_square(
            document_cv_img, match_result_viewport[0], match_result_viewport[1]
        )

        img_ref = cv2.resize(im_matched, frame_dsize)
        img_ref_bin = cvimutil.bgr_to_bin(img_ref)

        img_base = im_frame
        img_base_bin = cvimutil.bgr_to_bin(img_base)

        im_diff_bin = cv2.absdiff(img_ref_bin, img_base_bin)

        hist_comparison_bgr = cvimutil.compare_hists(img_ref, img_base)
        hist_comparison_bin = cvimutil.compare_hists(img_ref_bin, img_base_bin)

        h_pp_corr, v_pp_corr = cvimutil.calc_vh_projection_profile_corr(
            img_ref, img_base
        )

        PSNR_quality = compute_psnr(img_ref_bin, img_base_bin)
        SSIM_quality = compute_ssim(img_ref_bin, img_base_bin)
        MSE_quality = compute_mse(img_ref_bin, img_base_bin)
        # PSNR_quality, _ = compute_psnr(img_ref_bin, img_base_bin)
        # SSIM_quality, _ = compute_ssim(img_ref_bin, img_base_bin)
        # MSE_quality, _ = compute_mse(img_ref_bin, img_base_bin)
        # GMSD_quality, _ = cv2.quality.QualityGMSD().compute(
        #     img_ref_bin, img_base_
        # )

        result.append(
            {
                "frame_time": t,
                "im_frame": [
                    img_ref.shape,
                    cvimutil.cvt_to_dataurl(img_ref_bin),
                ],
                "im_matched": [
                    im_matched.shape,
                    cvimutil.cvt_to_dataurl(img_base_bin),
                ],
                "im_diff": [
                    im_diff_bin.shape,
                    cvimutil.cvt_to_dataurl(im_diff_bin),
                ],
                "qa_result": {
                    "ssim": SSIM_quality,
                    "psnr": PSNR_quality,
                    "mse": MSE_quality,
                    # "gmsd": GMSD_quality,
                    "hist_bgr": hist_comparison_bgr,
                    "hist_bin": hist_comparison_bin,
                    "h_pp_coeff": h_pp_corr,
                    "v_pp_coeff": v_pp_corr,
                },
            }
        )

    result_output_dir = paths.path_dir_output_front

    os.makedirs(result_output_dir, exist_ok=True)

    with open(
        os.path.join(
            result_output_dir,
            f"{asset_id}_scrolltl_qaresult.json",
        ),
        "w",
    ) as fp:
        json.dump(result, fp)

    return result


if __name__ == "__main__":
    targets = [
        AssetId.IEEEVR2022Ogawa,  # slide01
        AssetId.EdanMeyerVpt,  # doc01
    ]

    for target in targets:
        asset_id_str = get_asset_id(target)
        print(f"\nAttempt: {asset_id_str}")
        main(asset_id_str, (480, 240))
