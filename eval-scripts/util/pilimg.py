from PIL.Image import Image


def cvt_to_binary(pilimg: Image, bin_thresh=100, maxval=255):
    pilimg = pilimg.convert("L")
    return pilimg.point(lambda p: maxval if p > bin_thresh else 0)
