from PIL import Image
import numpy as np
from ft import dft2d, fourier_spectrum
from freq import filter2d_freq
import os
import sys

def f1(input_file, input_img):
    output_img = fourier_spectrum(input_img, 'DFT')
    # save output image
    f, e = os.path.splitext(input_file)
    output_file = f + "_dft" + e
    output_img.save(output_file)

def f2(input_file, input_img):
    im_matrix = np.array(input_img)
    output_matrix = dft2d(dft2d(im_matrix, 'DFT'), 'IDFT')
    output_img = Image.fromarray(output_matrix.real).convert("L")
    # save output image
    f, e = os.path.splitext(input_file)
    output_file = f + "_idft" + e
    output_img.save(output_file)

def f3(input_file, input_img):
    output_img = fourier_spectrum(input_img, 'FFT')
    # save output image
    f, e = os.path.splitext(input_file)
    output_file = f + "_fft" + e
    output_img.save(output_file)

def f4(input_file, input_img):
    im_matrix = np.array(input_img)
    output_matrix = dft2d(dft2d(im_matrix, 'FFT'), 'IFFT')
    output_img = Image.fromarray(output_matrix.real).convert("L")
    # save output image
    f, e = os.path.splitext(input_file)
    output_file = f + "_ifft" + e
    output_img.save(output_file)

def f5(input_file, input_img):
    im_matrix = np.array(input_img)
    filter_5_5 = (1 / 25) * np.ones((5, 5))
    output_matrix = filter2d_freq(im_matrix, filter_5_5)
    output_img = Image.fromarray(output_matrix).convert("L")
    # save output image
    f, e = os.path.splitext(input_file)
    output_file = f + "_filter_5-5" + e
    output_img.save(output_file)

def f6(input_file, input_img):
    im_matrix = np.array(input_img)
    filter_laplacian = np.array([
        [0, 1, 0],
        [1, -4, 1],
        [0, 1, 0]
    ])
    output_matrix = filter2d_freq(im_matrix, filter_laplacian)
    output_img = Image.fromarray(output_matrix).convert("L")
    # save output image
    f, e = os.path.splitext(input_file)
    output_file = f + "_filter_laplacian" + e
    output_img.save(output_file)

def main():
    input_file = sys.argv[1]
    input_img = Image.open(input_file).convert('L')
    f1(input_file, input_img)
    f2(input_file, input_img)
    f3(input_file, input_img)
    f4(input_file, input_img)
    f5(input_file, input_img)
    f6(input_file, input_img)

if __name__ == "__main__":
    main()