import configparser

import numpy as np
import pytest

from upa_matrix_builder import generate_pa_matrix, load_upa_from_one2one_file

config = configparser.ConfigParser()
config.read("config.ini")


def test__load_from_one2one_file__empty_file():
    test_matrix = load_upa_from_one2one_file("test_datasets/empty_dataset.txt")
    assert np.array_equal(test_matrix, np.zeros((0, 0)))


def test__load_from_one2one_file__identity_matrix():
    test_matrix = load_upa_from_one2one_file("test_datasets/identity_matrix.txt")
    assert np.array_equal(test_matrix, np.eye(5))


def test__load_from_one2one_file__simple_dataset():
    test_matrix_1 = load_upa_from_one2one_file("test_datasets/simple_dataset.txt")
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
        load_upa_from_one2one_file("test_datasets/not_exist.txt")


def test__generate_pa_matrix():
    max_permissions_per_role = 8
    num_of_roles = 10
    num_of_permissions = 12
    min_permissions_per_role = config.getint("permissions", "min_per_role")
    roles = generate_pa_matrix(
        num_of_roles=num_of_roles,
        num_of_permissions=num_of_permissions,
        max_permissions_per_role=max_permissions_per_role,
    )
    assert isinstance(roles, np.ndarray)
    assert len(roles) == num_of_roles
    for role in roles:
        print(f"Role: {role}  Sum:{sum(role)}")
        assert min_permissions_per_role <= sum(role) <= max_permissions_per_role
