from enum import Enum, auto


class AssetId(Enum):
    IEEEVR2022Ogawa = auto()
    IEEEVR2022Hoshikawa = auto()
    EdanMeyerVpt = auto()


def get_asset_id(asset_id: AssetId):
    match asset_id:
        case AssetId.IEEEVR2022Ogawa:
            return "IEEEVR2022Ogawa"

        case AssetId.IEEEVR2022Hoshikawa:
            return "IEEEVR2022Hoshikawa"

        case AssetId.EdanMeyerVpt:
            return "EdanMeyerVpt"

        case _:
            raise ValueError("Invalid asset id.")
