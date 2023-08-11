def get_bbox_dsize(bbox: list[list, list]) -> float:
    top = bbox[0][1]  # y1
    left = bbox[0][0]  # x1
    bottom = bbox[1][1]  # y2
    right = bbox[1][0]  # x2

    bbox_dsize = (right - left, bottom - top)

    assert (
        bbox_dsize[0] >= 0 and bbox_dsize[1] >= 0
    ), f"\nbbox_dsize values must be positive. \nResult: dsize = ({bbox_dsize}) \n"

    return bbox_dsize


def add_bbox(bbox1: list[list], bbox2: list[list]):
    return [
        [bbox1[0][0] + bbox2[0][0], bbox1[0][1] + bbox2[0][1]],
        [bbox1[1][0] + bbox2[1][0], bbox1[1][1] + bbox2[1][1]],
    ]


def apply_each(bbox, func):
    return [
        [func(bbox[0][0]), func(bbox[0][1])],
        [func(bbox[1][0]), func(bbox[1][1])],
    ]
