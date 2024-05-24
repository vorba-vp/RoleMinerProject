import configparser

import numpy as np
import pytest

from dataset import upa_matrix

config = configparser.ConfigParser()
config.read("config.ini")


def test__load_from_one2one_file__empty_file():
    test_matrix = upa_matrix.load_upa_from_one2one_file(
        "dataset/test_datasets/empty_dataset.txt"
    )
    assert np.array_equal(test_matrix, np.zeros((0, 0)))


def test__load_from_one2one_file__identity_matrix():
    test_matrix = upa_matrix.load_upa_from_one2one_file(
        "dataset/test_datasets/identity_matrix.txt"
    )
    assert np.array_equal(test_matrix, np.eye(5))


def test__load_from_one2one_file__simple_dataset():
    test_matrix_1 = upa_matrix.load_upa_from_one2one_file(
        "dataset/test_datasets/simple_dataset.txt"
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
        upa_matrix.load_upa_from_one2one_file("dataset/test_datasets/not_exist.txt")


def test__generate_pa_matrix():
    num_of_roles = 10
    num_of_permissions = 12
    max_permissions_per_role = 8
    min_permissions_per_role = config.getint("permissions", "min_per_role")
    roles = upa_matrix.generate_pa_matrix(
        num_of_roles=num_of_roles,
        num_of_permissions=num_of_permissions,
        max_permissions_per_role=max_permissions_per_role,
    )
    assert isinstance(roles, np.ndarray)
    assert len(roles) == num_of_roles
    for role in roles:
        assert min_permissions_per_role <= sum(role) <= max_permissions_per_role


def test__generate_upa_matrix():
    num_of_users = 20
    num_of_roles = 6
    num_of_permissions = 12
    max_roles_per_user = 1
    max_permissions_per_role = 8
    upa = upa_matrix.generate_upa_matrix(
        num_of_users=num_of_users,
        num_of_roles=num_of_roles,
        num_of_permissions=num_of_permissions,
        max_roles_per_user=max_roles_per_user,
        max_permissions_per_role=max_permissions_per_role,
    )
    assert len(upa) == num_of_users
    for u in upa:
        assert len(u) == num_of_permissions
        assert sum(u) <= max_permissions_per_role
    roles_set = set([tuple(u) for u in upa])
    assert len(roles_set) <= num_of_roles
