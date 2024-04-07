import numpy as np
import pytest

from upa_matrix_builder import UpaMatrixBuilder


def test__load_from_one2one_file__empty_file():
    test_matrix = UpaMatrixBuilder.load_from_one2one_file(
        "../test_datasets/empty_dataset.txt"
    )
    assert np.array_equal(test_matrix, np.zeros((0, 0)))


def test__load_from_one2one_file__identity_matrix():
    test_matrix = UpaMatrixBuilder.load_from_one2one_file(
        "../test_datasets/identity_matrix.txt"
    )
    assert np.array_equal(test_matrix, np.eye(5))


def test__load_from_one2one_file__simple_dataset():
    test_matrix_1 = UpaMatrixBuilder.load_from_one2one_file(
        "../test_datasets/simple_dataset.txt"
    )
    test_matrix_2 = np.array(
        [
            [1, 1, 0, 1],
            [0, 1, 1, 0],
            [1, 1, 0, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 1],
            [0, 1, 1, 1],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [1, 1, 0, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 1],
        ]
    )
    assert np.array_equal(test_matrix_1, test_matrix_2)


def test__load_from_one2one_file__non_existing_file():
    with pytest.raises(FileNotFoundError):
        UpaMatrixBuilder.load_from_one2one_file("../test_datasets/not_exist.txt")
