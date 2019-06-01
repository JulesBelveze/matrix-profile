import numpy as np
from scipy.fftpack import fft, ifft


def sliding_dot_product(time_series: np.array, query_sequence: np.array) -> np.array:
    """
    Computes the dot products of a query sequence of length M and every contiguous subsequence of length M in a
    time series of length N. Used in the distance calculations in Mueen's Algorithm for Similarity Search (MASS).

    The time complexity of directly computing the dot product of every subsequence starting at position 0, 1, ..., N-M
    with every other subsequence of equal length is O(n^2). Mueen's Algorithm reduces this to O(n log n) using Fast
    Fourier Transforms: the dot product of two vectors is the inverse Fourier transform of the dot product of their
    Fourier transforms and the time complexity of the Fast Fourier Transform is O(n log n).

    NB. The time complexity of this algorithm depends only on the length of the time series, not on the query sequence.
    This is a useful property: short patterns do not take more time to identify than long patterns.

    Citation: Keogh et al (2016): http://www.cs.ucr.edu/~eamonn/PID4481997_extend_Matrix%20Profile_I.pdf

    :param time_series: time series, length N
    :param query_sequence: query sequence, length M <= N
    :return: array of dot products of the query sequence with every subsequence of length M in the time series
    """

    # Compute the lengths of the time series (N) and query sequence (M)
    time_series_length = time_series.shape[0]
    query_sequence_length = query_sequence.shape[0]

    # Reverse the query sequence
    query_sequence = query_sequence[::-1]

    # Append the reversed query sequence with 0s, so that it is the same length as the time series
    query_sequence = np.append(query_sequence, np.zeros(time_series_length - query_sequence_length))

    # Take the Fast Fourier Transforms of the time series and the reversed query sequence
    time_series = fft(time_series)
    query_sequence = fft(query_sequence)

    # Obtain the transformed dot products of the query sequence with every subsequence of length M in the time series
    # by multiplying the Fourier transforms element-wise
    fourier_products = np.multiply(query_sequence, time_series)

    # Obtain the dot products of the query sequence with every subsequence of length M in the time series by applying
    # the inverse Fast Fourier Transform
    dot_products = np.real(ifft(fourier_products))

    # Discard incomplete windows
    dot_products = dot_products[query_sequence_length-1: time_series_length]

    return dot_products


def rolling_mean(time_series: np.array, window_length: int) -> np.array:
    """
    Computes the rolling mean of a time series for a specified window length

    :param time_series: time series
    :param window_length: window length
    :return: array of rolling means, from the first complete window onwards
    """

    # Compute the cumulative sum of the time series
    rolling = np.cumsum(time_series, dtype=float)

    # At each position, subtract the cumulative sum of the time series prior to the window
    rolling[window_length:] = rolling[window_length:] - rolling[:-window_length]

    # Discard incomplete windows
    rolling = rolling[window_length - 1:]

    # Divide by the window length to obtain the mean
    rolling = rolling / window_length

    return rolling
