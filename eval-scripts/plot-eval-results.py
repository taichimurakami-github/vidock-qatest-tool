import os
import json
import util.paths as paths
from util.asset import AssetId, get_asset_id
import util.plot as pltutil


def main(asset_id: str):
    print(paths.path_dir_output_front)
    with open(
        os.path.join(
            paths.path_dir_output_front, f"{asset_id}_scrolltl_qaresult.json"
        ),
        "r",
    ) as fp:
        result = json.load(fp)

    os.makedirs(paths.path_dir_output_back, exist_ok=True)

    # Draw scatter plots
    plot_target_keys = result[0]["qa_result"].keys()
    time = [v["frame_time"] for v in result]
    for key in plot_target_keys:
        plt_values = [v["qa_result"][key] for v in result]

        # exclude n-dim data (n > 1)
        if key == "hist_bgr":
            continue

        title = f"{asset_id}_{key}_plot"

        pltutil.plot_scatter(
            x=time,
            y=plt_values,
            title=title,
            ylabel=key,
            save_path=os.path.join(
                paths.path_dir_output_front, f"{title}.png"
            ),
        )


if __name__ == "__main__":
    targets = [
        AssetId.IEEEVR2022Ogawa,  # slide01
        AssetId.EdanMeyerVpt,  # doc01
    ]

    for target in targets:
        asset_id_str = get_asset_id(target)
        print(f"\nAttempt: {asset_id_str}")
        main(asset_id_str)
