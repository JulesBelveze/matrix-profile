from matrix_profile.mass import sliding_dot_product, rolling_mean, distance, mass
import numpy as np
from unittest import TestCase


class TestMASS(TestCase):

    def test_sliding_dot_product(self):
        time_series = np.arange(100)
        query_sequence = np.array([1, 2, 3])
        dot_products = sliding_dot_product(time_series, query_sequence)

        # The correct result is [8, 14, 20, ..., 590]
        expected_output = np.array([n + 2*(n+1) + 3*(n+2) for n in range(len(time_series) - len(query_sequence) + 1)])

        # Comparison of float array with int array
        np.testing.assert_array_almost_equal(dot_products, expected_output, decimal=7)

    def test_rolling_mean(self):
        time_series = np.arange(100)
        ts_mean = rolling_mean(time_series, 2)

        # The correct result is [0.5, 1.5, ..., 99.5]
        expected_output = np.array([n + 0.5 for n in range(len(time_series) - 1)])
        np.testing.assert_array_equal(ts_mean, expected_output)
