import os
import skimage.io



def slice_im_plus_boxes(image_path, out_dir_images):
    imagesize = 640
    overlap = 0.2
    image = skimage.io.imread(image_path)
    dx = int((1. - overlap) * imagesize)
    dy = int((1. - overlap) * imagesize)
    n_ims = 0
    index = 0

    for y0 in range(0, image.shape[0], dy):
        for x0 in range(0, image.shape[1], dx):
            n_ims += 1
            index += 1

            # if (n_ims % 100) == 0:
            # print(n_ims)

            if y0 + imagesize > image.shape[0]:
                y = image.shape[0] - imagesize
            else:
                y = y0
            if x0 + imagesize > image.shape[1]:
                x = image.shape[1] - imagesize
            else:
                x = x0

            window_c = image[y:y + imagesize, x:x + imagesize]
            # if index < 10:
            #     outpath = os.path.join(
            #         out_dir_images,
            #         out_name + '_0' + str(index) + '_' + str(y) + '_' + str(x) + '.jpg')
            # else:
            #     outpath = os.path.join(
            #         out_dir_images,
            #         out_name + '_' + str(index) + '_' + str(y) + '_' + str(x) + '.jpg')
            outpath = os.path.join(
                out_dir_images,
                os.path.basename(image_path).split('.')[0] + '_' + str(y) + '_' + str(x) + '.jpg')
            if not os.path.exists(outpath):
                skimage.io.imsave(outpath, window_c, check_contrast=False)
            else:
                print("outpath {} exists, skipping".format(outpath))
    return


if __name__ == '__main__':
    slice_im_plus_boxes('/Users/lixiang/Projects/test/JL1GF02A_PMS1_20210609175921_200052417_102_0002_001_L3D_PSH_2.jpg', '/Users/lixiang/Projects/test/images640/')
