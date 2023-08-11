from matplotlib import pyplot as plt
import numpy as np
from typing import Iterable


def plot_scatter(
    x: Iterable[float | int],
    y: Iterable[float | int],
    title: str,
    ylabel: str,
    xlabel: str = "time",
    save_path=None,
):
    plt.title(title)
    plt.xlabel("time")
    plt.scatter(x, y)

    if save_path != None:
        plt.savefig(save_path)

    plt.cla()

    return
