from PIL import Image
import numpy as np

def dft2d(matrix, flags):
    """Compute the DFT/FFT or IDFT/IFFT of the matrix according to flags"""
    if flags == 'DFT':
        return fourier_2d(matrix)
    elif flags == 'IDFT':
        return inverse_fourier_2d(matrix)
    elif flags == 'FFT':
        return fast_fourier_2d(matrix)
    elif flags == 'IFFT':
        return inverse_fast_fourier_2d(matrix)

# ==========================================================================

def fourier_spectrum(im, flags):
    """Get the Fourier spectrum of the given image"""
    matrix = np.array(im)
    matrix = dft2d(matrix, flags)
    matrix = np.fft.fftshift(matrix)
    matrix = np.log(1 + np.abs(matrix))
    matrix = quantize(matrix)
    return Image.fromarray(matrix).convert("L")

def quantize(matrix):
    """Quantize the matrix"""
    M, N = matrix.shape
    factor = (matrix.max() - matrix.min()) / 256
    for row in range(M):
        for col in range(N):
            matrix[row, col] = round(matrix[row, col] / factor)
    return matrix

# ==========================================================================

def fourier_2d(matrix):
    """Compute the discrete Fourier Transform of the matrix"""
    M, N = matrix.shape
    output_matrix = np.zeros((M, N), dtype=np.complex)
    for row in range(M):
        output_matrix[row, :] = fourier_1d(matrix[row])
    for col in range(N):
        output_matrix[:, col] = fourier_1d(output_matrix[:, col])
    return output_matrix

def inverse_fourier_2d(matrix):
    """Compute the inverse discrete Fourier Transform of the matrix"""
    M, N = matrix.shape
    output_matrix = np.zeros((M, N), dtype=np.complex)
    for row in range(M):
        output_matrix[row, :] = inverse_fourier_1d(matrix[row])
    for col in range(N):
        output_matrix[:, col] = inverse_fourier_1d(output_matrix[:, col])
    return output_matrix

def fourier_1d(arr):
    """Compute the discrete Fourier Transform of the 1D array"""
    N = arr.shape[0]
    # [0, 1, 2, ... , N - 1]
    x = np.arange(N).reshape((1, N))
    # transpose of x
    u = x.reshape((N, 1))
    # e ^ (-j * 2 * π * u * x / N)
    E = np.exp(-1j * 2 * np.pi * np.dot(u, x) / N)
    return np.dot(E, arr)

def inverse_fourier_1d(arr):
    """Compute the inverse discrete Fourier Transform of the 1D array"""
    N = arr.shape[0]
    # [0, 1, 2, ... , N - 1]
    x = np.arange(N).reshape((1, N))
    # transpose of x
    u = x.reshape((N, 1))
    # e ^ (j * 2 * π * u * x / N)
    E = np.exp(1j * 2 * np.pi * np.dot(u, x) / N)
    return np.dot(E, arr) / N

# ==========================================================================

def fast_fourier_2d(matrix):
    """Compute the discrete Fourier Transform of the matrix"""
    M, N = matrix.shape
    output_matrix = np.zeros((M, N), dtype=np.complex)
    for row in range(M):
        output_matrix[row, :] = fast_fourier_1d(matrix[row])
    for col in range(N):
        output_matrix[:, col] = fast_fourier_1d(output_matrix[:, col])
    return output_matrix

def inverse_fast_fourier_2d(matrix):
    """Compute the inverse discrete Fourier Transform of the matrix"""
    M, N = matrix.shape
    output_matrix = np.zeros((M, N), dtype=np.complex)
    for row in range(M):
        output_matrix[row, :] = inverse_fast_fourier_1d(matrix[row])
    for col in range(N):
        output_matrix[:, col] = inverse_fast_fourier_1d(output_matrix[:, col])
    return output_matrix

def fast_fourier_1d(arr):
    """Compute the discrete Fourier Transform of the 1D array"""
    arr = np.asarray(arr, dtype=np.complex)
    N = arr.shape[0]
    if N % 2 > 0:
        return fourier_1d(arr)
    else:
        even_part = fast_fourier_1d(arr[::2])
        odd_part = fast_fourier_1d(arr[1::2])
        factor = np.exp(-1j * 2 * np.pi * np.arange(N) / N)
        return np.concatenate([even_part + factor[: N // 2] * odd_part,
                            even_part + factor[N // 2 :] * odd_part])

def inverse_fast_fourier_1d(arr):
    """Compute the inverse discrete Fourier Transform of the 1D array"""
    def rec(arr):
        arr = np.asarray(arr, dtype=np.complex)
        N = arr.shape[0]
        if N % 2 > 0:
            return inverse_fourier_1d(arr) * N
        else:
            even_part = rec(arr[::2])
            odd_part = rec(arr[1::2])
            factor = np.exp(1j * 2 * np.pi * np.arange(N) / N)
            return np.concatenate([even_part + factor[: N // 2] * odd_part,
                                even_part + factor[N // 2 :] * odd_part])
    return rec(arr) / arr.shape[0]