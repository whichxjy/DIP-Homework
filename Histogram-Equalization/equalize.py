from PIL import Image
import numpy as np
import os
import sys

def equalize_hist(input_img):
    # image array
    im_matrix = np.array(input_img)
    # create a histogram of the image
    hist = np.zeros(256)
    count = 0
    for row in im_matrix:
        for gray_data in row:
            hist[gray_data] += 1
            count += 1
    hist = hist / count
    # accumulative frequency
    acc_freq = np.zeros(256)
    acc_freq[0] = hist[0]
    for i in range(1, 256):
        acc_freq[i] = acc_freq[i - 1] + hist[i]
    # transformation array
    trans = (acc_freq * 255).astype(int)
    # histogram equalization
    for i, row in enumerate(im_matrix):
        for j, gray_data in enumerate(row):
            im_matrix[i][j] = trans[gray_data]
    return Image.fromarray(im_matrix).convert("L")

def main():
    # image
    input_file = sys.argv[1]
    input_img = Image.open(input_file).convert('L')
    # histogram equalization
    output_img = equalize_hist(input_img)
    # save output image
    f, e = os.path.splitext(input_file)
    output_file = f + "_eh" + e
    output_img.save(output_file)

if __name__ == "__main__":
    main()