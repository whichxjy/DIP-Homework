import numpy as np
from ft import dft2d

def filter2d_freq(matrix, filter):
    M, N = matrix.shape
    M_f, N_f = filter.shape
    P, Q = M * 2, N * 2

    # padded matrix
    pad_matrix = np.zeros((P, Q))
    pad_matrix[:M, :N] = matrix
    # shifted matrix
    shifted_matrix = shift(pad_matrix)
    # fft matrix
    fft_matrix = dft2d(shifted_matrix, 'FFT')

    # padded filter
    pad_filter = np.zeros((P, Q))
    pad_filter[:M_f, :N_f] = filter
    # shifted filter
    shifted_filter = shift(pad_filter)
    # fft filter
    fft_filter = dft2d(shifted_filter, 'FFT')

    # filtering in the Frequency Domain
    g_matrix = fft_matrix * fft_filter

    # ifft
    ifft_matrix = dft2d(g_matrix, 'IFFT')
    # shift ifft matrix
    shifted_ifft_matrix = shift(ifft_matrix)
    return shifted_ifft_matrix.real[:M, :N]

def shift(matrix):
    M, N = matrix.shape
    x = np.arange(M).reshape((M, 1))
    y = np.arange(N).reshape((1, N))
    return (-1) ** (x + y) * matrix