from PIL import Image
import numpy as np
import os
import sys

def filter2d(input_img, filter):
    # image array
    im_matrix = np.array(input_img)
    row, col = im_matrix.shape
    # zero padding
    filter_size = filter.shape[0]
    padding_size = filter_size // 2
    padding_im_matrix = zero_padding(im_matrix, padding_size)
    # convolution
    reverse_filter = np.flip(filter)
    convol_matrix = np.zeros((row + 2 * padding_size, col + 2 * padding_size))
    for i in range(padding_size, padding_size + row):
        for j in range(padding_size, padding_size + col):
            submatrix = padding_im_matrix[i - padding_size : i + padding_size + 1,
                                          j - padding_size : j + padding_size + 1]
            convol_matrix[i][j] = round((submatrix * reverse_filter).sum())
    # output
    output_im_matrix = convol_matrix[padding_size : padding_size + row,
                                     padding_size : padding_size + col]
    return Image.fromarray(output_im_matrix).convert("L")

def zero_padding(matrix, padding_size):
    row, col = matrix.shape
    new_matrix = np.zeros((row + 2 * padding_size, col + 2 * padding_size))
    new_matrix[padding_size : padding_size + row, padding_size : padding_size + col] = matrix
    return new_matrix

def high_boost_filtering(input_img, filter, k):
    im_matrix = np.array(input_img)
    blurred_im_matrix = np.array(filter2d(input_img, filter))
    mask_matrix = im_matrix - blurred_im_matrix
    return Image.fromarray(im_matrix + k * mask_matrix).convert("L")

def main():
    # image
    input_file = sys.argv[1]
    input_img = Image.open(input_file).convert('L')
    # filters
    # filter_3_3 = np.ones((3, 3)) / 9
    # filter_5_5 = np.ones((5, 5)) / 25
    # filter_7_7 = np.ones((7, 7)) / 49
    filter_laplacian = np.array([[1, 1, 1],
                                 [1, -8, 1],
                                 [1, 1, 1]])
    # spatial-filtering
    output_img = filter2d(input_img, filter_laplacian)
    # save output image
    f, e = os.path.splitext(input_file)
    output_file = f + "_sf" + e
    output_img.save(output_file)

if __name__ == "__main__":
    main()