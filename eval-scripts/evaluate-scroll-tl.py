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
import ssim.ssimlib as pyssim
import util.paths as paths
import util.video as vutil
from util.asset import AssetId, get_asset_id
import util.cvimg as cvimutil
import util.plot as pltutil
import util.text as txtutil
from util.ocr import OcrTextExtractor, cvt_lbbox_list_to_joined_str


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
def main(asset_id: str, tesseract_path: str, resize_width_px=None):
    print(asset_id)
    cap = vutil.get_cv_video_cap(paths.path_file_video(asset_id))

    document_scroll_tl = None
    with open(paths.path_file_scroll_tl(asset_id), "r") as fp:
        document_scroll_tl = json.load(fp)["tl_document_scrollY"]

    document_cv_img = cv2.imread(paths.path_file_document_concat_img(asset_id))
    print(f"document img shape: {document_cv_img.shape}")

    en_lbbox_tesseract = (
        OcrTextExtractor(tesseract_path)
        .use_english_lang()
        .use_linebox_builder()
    )

    result = []

    for section in document_scroll_tl:
        if section[1] == None:
            continue

        t = section[0]
        match_result_viewport = section[-1]

        print(f"Analyzing frame t = {t}")

        im_frame = vutil.get_frame_as_cv_img(cap, t * 1000)

        if resize_width_px != None:
            resize_dsize = (
                resize_width_px,
                int(resize_width_px * im_frame.shape[0] / im_frame.shape[1]),
            )
            print("Resize to : ", resize_dsize)
            im_frame = cv2.resize(im_frame, resize_dsize)

        frame_dsize = im_frame.shape[1], im_frame.shape[0]

        im_matched = cvimutil.imcrop_around_square(
            document_cv_img, match_result_viewport[0], match_result_viewport[1]
        )

        img_from_doc = cv2.resize(im_matched, frame_dsize)
        img_from_doc_bin = cvimutil.bgr_to_bin(img_from_doc)
        img_from_doc_bin_pil = cvimutil.cvt_to_pilimg(img_from_doc_bin)
        img_from_doc_contents_joined = cvt_lbbox_list_to_joined_str(
            en_lbbox_tesseract.extract(img_from_doc_bin_pil)
        )

        img_from_video = im_frame
        img_from_video_bin = cvimutil.bgr_to_bin(img_from_video)
        img_from_video_bin_pil = cvimutil.cvt_to_pilimg(img_from_video_bin)
        img_from_video_contents_joined = cvt_lbbox_list_to_joined_str(
            en_lbbox_tesseract.extract(img_from_video_bin_pil)
        )

        img_diff_bin = cv2.absdiff(img_from_doc_bin, img_from_video_bin)

        hist_comparison_bgr = cvimutil.compare_hists(
            img_from_doc, img_from_video
        )
        hist_comparison_bin = cvimutil.compare_hists(
            img_from_doc_bin, img_from_video_bin
        )

        h_pp_corr, v_pp_corr = cvimutil.calc_vh_projection_profile_corr(
            img_from_doc, img_from_video
        )

        MSE_quality = compute_mse(img_from_doc_bin, img_from_video_bin)
        PSNR_quality = compute_psnr(img_from_doc_bin, img_from_video_bin)
        SSIM_quality = compute_ssim(img_from_doc_bin, img_from_video_bin)
        CW_SSIM_quality = pyssim.SSIM(img_from_doc_bin_pil).cw_ssim_value(
            img_from_video_bin_pil
        )

        content_similarity_bigram = txtutil.get_ngram_score(
            img_from_video_contents_joined, img_from_doc_contents_joined
        )

        # PSNR_quality, _ = compute_psnr(img_from_doc_bin, img_from_video_bin)
        # SSIM_quality, _ = compute_ssim(img_from_doc_bin, img_from_video_bin)
        # MSE_quality, _ = compute_mse(img_from_doc_bin, img_from_video_bin)
        # GMSD_quality, _ = cv2.quality.QualityGMSD().compute(
        #     img_from_doc_bin, img_from_video_
        # )

        result.append(
            {
                "frame_time": t,
                "im_frame": [
                    im_matched.shape,
                    cvimutil.cvt_to_dataurl(img_from_video_bin),
                ],
                "im_matched": [
                    img_from_doc.shape,
                    cvimutil.cvt_to_dataurl(img_from_doc_bin),
                ],
                "im_diff": [
                    img_diff_bin.shape,
                    cvimutil.cvt_to_dataurl(img_diff_bin),
                ],
                "qa_result": {
                    "contents_similarity_bigram": content_similarity_bigram,
                    "ssim": SSIM_quality,
                    "cw_ssim": CW_SSIM_quality,
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
    # result_output_dir = paths.path_dir_output_back

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
        main(asset_id_str, paths.path_file_tessearct_bin, 960)
