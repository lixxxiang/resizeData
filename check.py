import os
from PIL import Image
from PIL import ImageDraw, ImageFont
import numpy as np
from main import *


def check(label_path, images_path):
    for root, dirs, files in os.walk(label_path):
        for file in files:
            voc = []
            check_jpg = Image.open(os.path.join(images_path, os.path.basename(file).split('.')[0] + '.jpg'))
            jpg2 = ImageDraw.Draw(check_jpg)
            for line in open(os.path.join(root, file), 'rb').readlines():
                data = []
                bbox_width = float(line.decode().split(' ')[3]) * 640
                bbox_height = float(line.decode().split(' ')[4]) * 640
                center_x = float(line.decode().split(' ')[1]) * 640
                center_y = float(line.decode().split(' ')[2]) * 640
                data.append(float(line.decode().split(' ')[0]))
                data.append(center_x - (bbox_width / 2))
                data.append(center_y - (bbox_height / 2))
                data.append(center_x + (bbox_width / 2))
                data.append(center_y + (bbox_height / 2))
                voc.append(data)
                for i in range(len(voc)):
                    plot_box(jpg2, voc[i][1], voc[i][2], voc[i][3], voc[i][4], None, (65, 105, 225), 3)
            check_jpg.convert('RGB').save(os.path.join('/Users/lixiang/Projects/test/check640/', os.path.basename(file).split('.')[0] + '.jpg'))


if __name__ == '__main__':
    check('/Users/lixiang/Projects/test/labels640/', '/Users/lixiang/Projects/test/images640/')
