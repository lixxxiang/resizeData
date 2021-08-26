from utils import *


def clearRotate():
    for root, dirs, files in os.walk('/Users/lixiang/Projects/test/labels'):
        for file in files:
            print(os.path.join(root, file))
            filename = os.path.splitext(file)[0]
            if str(filename).split('_')[-1] == '90d' or str(filename).split('_')[-1] == '270d' or \
                    str(filename).split('_')[-1] == '180d':
                os.remove(os.path.join(root, file))


def draw(raw_jpg):
    data = []

    before_nms_jpg = Image.open(raw_jpg)
    after_nms_jpg = Image.open(raw_jpg)
    jpg2 = ImageDraw.Draw(before_nms_jpg)
    jpg3 = ImageDraw.Draw(after_nms_jpg)
    for root, dirs, files in os.walk(r'/Users/lixiang/Projects/test/labels'):
        for file in files:
            if file != '.DS_Store':
                data = restore(os.path.join(root, file), raw_jpg, data)
    # for i in range(len(data)):
    #     plot_box(jpg2, data[i][1], data[i][2], data[i][3], data[i][4], None, (65, 105, 225), 3)
    # before_nms_jpg.convert('RGB').save(
    #     os.path.join('/Users/lixiang/Projects/test/', 'before_' + os.path.basename(raw_jpg)))
    data = manual_nms(data)
    data = NMS(data, thresh=0.1)

    print(len(data))
    # for i in range(len(data)):
    #     plot_box(jpg3, data[i][1], data[i][2], data[i][3], data[i][4], None, (65, 105, 225), 3)
    # after_nms_jpg.convert('RGB').save(os.path.join('/Users/lixiang/Projects/test/', 'nms_' + os.path.basename(raw_jpg)))
    for i in range(len(data)):
        width = data[i][1] // 512 * 512
        height = data[i][2] // 512 * 512
        # plot_box(jpg3, data[i][1], data[i][2], data[i][3], data[i][4], None, (65, 105, 225), 10)
        # after_nms_jpg.convert('RGB').save(os.path.join('D:\global-test\global-test\\', 'after_' + os.path.basename(raw_jpg)))
        file = open(
            '/Users/lixiang/Projects/test/labels640/{}_{}_{}.txt'.format(os.path.basename(raw_jpg).split('.')[0],
                                                                         int(height), int(width)), 'a')
        box = []
        # print(width)
        # print(height)
        # print(data[i][1] % 512)
        # print(data[i][3] % 512)
        box.append(data[i][1] % 512)
        box.append(data[i][3] % 512)
        box.append(data[i][2] % 512)
        box.append(data[i][4] % 512)
        x, y, w, h = convert([640, 640], box)
        print('{}-{} x, y, w, h {} {} {} {}'.format(int(width), int(height), ('%.6f' % x), ('%.6f' % y), ('%.6f' % w),
                                                    ('%.6f' % h)))
        file.write('{} {} {} {} {}\n'.format(int(data[i][0]), ('%.6f' % x), ('%.6f' % y), ('%.6f' % w), ('%.6f' % h)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    draw('/Users/lixiang/Projects/test/JL1GF02A_PMS1_20210609175921_200052417_102_0002_001_L3D_PSH_2.jpg')
    # clearRotate()
