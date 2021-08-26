# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
from PIL import Image
from PIL import ImageDraw, ImageFont
import numpy as np


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def NMS(data, thresh):
    x1 = np.zeros(len(data))
    y1 = np.zeros(len(data))
    x2 = np.zeros(len(data))
    y2 = np.zeros(len(data))
    scores = np.zeros(len(data))
    for i in range(len(data)):
        x1[i] = data[i][1]
        y1[i] = data[i][2]
        x2[i] = data[i][3]
        y2[i] = data[i][4]
        scores[i] = data[i][5]
    areas = (y2 - y1 + 1) * (x2 - x1 + 1)
    # scores = bboxs[:, 4]
    index = scores.argsort()[::-1]
    res = []
    while index.size > 0:
        i = index[0]
        res.append(i)
        x11 = np.maximum(x1[i], x1[index[1:]])
        y11 = np.maximum(y1[i], y1[index[1:]])
        x22 = np.minimum(x2[i], x2[index[1:]])
        y22 = np.minimum(y2[i], y2[index[1:]])
        w = np.maximum(0, x22 - x11 + 1)
        h = np.maximum(0, y22 - y11 + 1)
        overlaps = w * h
        ious = overlaps / (areas[i] + areas[index[1:]] - overlaps)
        idx = np.where(ious <= thresh)[0]
        index = index[idx + 1]
    data2 = []
    for i in range(len(res)):
        data2.append(data[res[i]])
    return data2


def plot_box(jpg, xl, yl, xr, yr, fill, color, width):
    jpg.rectangle([xl, yl, xr, yr], fill=fill, outline=color, width=width)


def plot_tag(jpg, xl, yl, xr, yr, label, fill, color, width, tag_width, text_size):
    font = ImageFont.truetype(r"C:\Windows\Fonts\Calibrib.ttf", 12)
    if text_size == 12:
        jpg.rectangle([xl, yl - text_size[1], xr + tag_width, yr], fill=fill, outline=color, width=width)
    else:
        jpg.rectangle([xl, yl - text_size[1], xl + tag_width, yl], fill=fill, outline=color, width=width)
    jpg.text((xl, yl - text_size[1]), label, font=font, fill=(255, 255, 255))


def calc_shape(data):
    w = 0
    h = 0
    for i in range(len(data)):
        w += data[i][3] - data[i][1]
        h += data[i][4] - data[i][2]
    return w / h


def restore(file, raw_jpg, data):
    w = 416
    h = 416

    width = float(os.path.basename(file).split('_')[-1].split('.')[0])
    height = float(os.path.basename(file).split('_')[-2])
    # print("{} {}".format(width, height))
    raw_width, raw_height = Image.open(raw_jpg).size

    for line in open(file, 'rb').readlines():
        line = line.decode().strip('\n')
        temp_data = np.zeros(6)
        xl_temp = (float(line.split(' ')[1]) - 0.5 * float(line.split(' ')[3])) * w
        yl_temp = (float(line.split(' ')[2]) - 0.5 * float(line.split(' ')[4])) * h
        xr_temp = (float(line.split(' ')[1]) + 0.5 * float(line.split(' ')[3])) * w
        yr_temp = (float(line.split(' ')[2]) + 0.5 * float(line.split(' ')[4])) * h
        # confidence = float(line.split(' ')[5][0:4])
        classid = int(line.split(' ')[0])

        if width <= raw_width:
            xl = xl_temp + width
            xr = xr_temp + width
        else:
            xl = xl_temp
            xr = xr_temp
        if height <= raw_height:
            yl = yl_temp + height
            yr = yr_temp + height
        else:
            yl = yl_temp
            yr = yr_temp
        # if (XR - XL) / (YR - YL) < 3 and (YR - YL) / (XR - XL) < 3:
        temp_data[0] = classid
        temp_data[1] = xl
        temp_data[2] = yl
        temp_data[3] = xr
        temp_data[4] = yr
        # temp_data[5] = confidence
        data.append(temp_data)

    return data


def same(i, j):
    return abs(i - j) < 10


def reset_data(data):
    for i in range(len(data)):
        data[i] = 0
    return data


def manual_nms(data):
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            # 上/下/左/右
            if same(data[i][1], data[j][1]) and same(data[i][2], data[j][2]) and same(data[i][4], data[j][4]):
                data[i][3] = max(data[i][3], data[j][3])
                data[j] = reset_data(data[j])
            if same(data[i][2], data[j][2]) and same(data[i][3], data[j][3]) and same(data[i][4], data[j][4]):
                data[i][1] = min(data[i][1], data[j][1])
                data[j] = reset_data(data[j])
            if same(data[i][1], data[j][1]) and same(data[i][3], data[j][3]) and same(data[i][4], data[j][4]):
                data[i][2] = min(data[i][2], data[j][2])
                data[j] = reset_data(data[j])
            if same(data[i][1], data[j][1]) and same(data[i][2], data[j][2]) and same(data[i][3], data[j][3]):
                data[i][4] = max(data[i][4], data[j][4])
                data[j] = reset_data(data[j])
            # 左上/左下/右上/右下
            # same xl yl, big xr big yr.
            if same(data[i][1], data[j][1]) and same(data[i][2], data[j][2]):
                data[i][3] = max(data[i][3], data[j][3])
                data[i][4] = max(data[i][4], data[j][4])
                data[j] = reset_data(data[j])
            # same xl yr, big xr small yl
            if same(data[i][1], data[j][1]) and same(data[i][4], data[j][4]):
                data[i][2] = min(data[i][2], data[j][2])
                data[i][3] = max(data[i][3], data[j][3])
                data[j] = reset_data(data[j])
            # same xr, yl, small xl big yr
            if same(data[i][2], data[j][2]) and same(data[i][3], data[j][3]):
                data[i][1] = min(data[i][1], data[j][1])
                data[i][4] = max(data[i][4], data[j][4])
                data[j] = reset_data(data[j])
            # same xr, yr, small xl small yl
            if same(data[i][3], data[j][3]) and same(data[i][4], data[j][4]):
                data[i][1] = min(data[i][1], data[j][1])
                data[i][2] = min(data[i][2], data[j][2])
                data[j] = reset_data(data[j])
            # if same(data[i][1], data[j][1]) and same(data[i][3], data[j][3]):
            #     data[i][2] = min(data[i][2], data[j][2])
            #     data[i][4] = max(data[i][4], data[j][4])

            if same(data[i][2], data[j][2]) and data[i][1] > data[j][1] and data[i][3] < data[j][3] and data[i][4] < \
                    data[j][4]:
                data[i] = reset_data(data[i])
            if same(data[i][2], data[j][2]) and data[i][1] < data[j][1] and data[i][3] > data[j][3] and data[i][4] > \
                    data[j][4]:
                data[j] = reset_data(data[j])
            if same(data[i][2], data[j][2]) and same(data[i][4], data[j][4]):
                if data[i][1] < data[j][1] < data[i][1] + (data[i][3] - data[i][1]) / 2 < data[i][3] < data[j][3]:
                    data[i][3] = data[j][3]
                    data[i][4] = data[j][4]
                    data[j] = reset_data(data[j])
                elif data[j][1] < data[i][1] < data[j][0] + (data[j][3] - data[j][1]) / 2 < data[j][3] < data[i][3]:
                    data[i][1] = data[j][1]
                    data[i][2] = data[j][2]
                    data[j] = reset_data(data[j])

            if same(data[i][1], data[j][1]) and same(data[i][3], data[j][3]):
                if (data[i][2] < data[j][2] < data[i][4] < data[j][4]) or (
                        data[j][2] < data[i][2] < data[j][4] < data[i][4]):
                    data[i][2] = min(data[i][2], data[j][2])
                    data[i][4] = max(data[i][4], data[j][4])
                    data[j] = reset_data(data[j])
            if same(data[i][2], data[j][2]) and same(data[i][4], data[j][4]):
                if (data[i][1] < data[j][1] < data[i][3] < data[j][3]) or (
                        data[j][1] < data[i][1] < data[j][3] < data[i][3]):
                    data[i][1] = min(data[i][1], data[j][1])
                    data[i][3] = max(data[i][3], data[j][3])
                    data[j] = reset_data(data[j])

        if data[i][4] - data[i][2] != 0:
            if (data[i][3] - data[i][1]) / (data[i][4] - data[i][2]) > 3 / 2 * calc_shape(data) or (
                    data[i][3] - data[i][1]) / (data[i][4] - data[i][2]) < 2 / 3 * calc_shape(data):
                data[i] = reset_data(data[i])
    return data
