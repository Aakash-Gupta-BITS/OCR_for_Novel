from PIL import Image, ImageFilter, ImageOps
from collections import deque as queue
import matplotlib.pyplot as plt
import numpy as np
import os
from io import BytesIO


def split_image(img_arr, split_window=0, vertical_cut: bool = False):
    if vertical_cut is True: img_arr = np.transpose(img_arr)

    sum_0 = [True] * (len(img_arr) + 1)
    for i, row_sum in enumerate(img_arr.sum(axis=1)):
        sum_0[i + 1] = (row_sum == 0)

    i = 1
    
    # Define which row to keep and which to eliminate
    while i < len(sum_0):
        if not sum_0[i]:
            i = i + 1
            continue

        j = i
        while j < len(sum_0) and sum_0[j]:
            j = j + 1

        l = j - i
        assert(l > 0)
        if l < split_window:
            for k in range(l):
                sum_0[i + k] = False

        i += l

    keep = []
    rem = []

    for i in range(1, len(sum_0)):
        if (not sum_0[i]) and sum_0[i - 1]:
            if len(keep) > 0 and vertical_cut:
                keep[-1] = np.transpose(keep[-1])
            keep.append([])
        if not sum_0[i]:
            keep[-1].append(img_arr[i - 1])
        else:
            rem.append(img_arr[i - 1])

    if len(keep) > 0 and vertical_cut:
        keep[-1] = np.transpose(keep[-1])

    return keep, rem


if __name__ == "__main__":
    clean_path = './clean_images/'
    dir_path = './images/'
    file_names = os.listdir(dir_path)
    file_names.sort()
    clean_images = [[Image.open(clean_path + x) for x in file_names][0]]
    arr = np.asarray(clean_images[0])
    if arr.mean() > 128:
        arr = 255 - arr
    x = split_image(np.asarray(arr))