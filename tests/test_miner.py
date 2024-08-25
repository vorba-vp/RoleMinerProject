import numpy as np

from algorithms.fast_miner import get_fast_miner_result
from algorithms.miner_utils import (
    get_fm_candidate_roles_total_count,
    get_fm_gen_roles,
    get_init_roles,
)
from algorithms.rmp import basic_rmp
from dataset.upa_matrix import load_upa_from_one2one_file


def test__fast_miner__simple__dataset():
    test_data = {
        "INIT_ROLES": np.array(
            [[1, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [0, 0, 0, 1]]
        ),
        "ORIGINAL_COUNT": {
            (1, 1, 0, 1): 5,
            (0, 1, 1, 0): 3,
            (0, 1, 1, 1): 3,
            (0, 0, 0, 1): 2,
        },
        "GEN_ROLES": np.array(
            [
                [1, 1, 0, 1],
                [0, 1, 0, 0],
                [0, 1, 0, 1],
                [0, 0, 0, 1],
                [0, 1, 1, 0],
                [0, 1, 1, 1],
            ]
        ),
        "TOTAL_COUNT": {
            (1, 1, 0, 1): 5,
            (0, 1, 0, 0): 11,
            (0, 1, 0, 1): 8,
            (0, 0, 0, 1): 10,
            (0, 1, 1, 0): 6,
            (0, 1, 1, 1): 3,
        },
    }

    upa = load_upa_from_one2one_file("dataset/test_datasets/simple_dataset.txt")

    init_roles, original_count = get_init_roles(upa)
    assert init_roles is not None
    assert np.array_equal(init_roles, test_data["INIT_ROLES"])
    for role_label, count in original_count.items():
        assert role_label in test_data["ORIGINAL_COUNT"]
        assert count == test_data["ORIGINAL_COUNT"][role_label]

    gen_roles = get_fm_gen_roles(init_roles)
    assert gen_roles is not None
    assert np.array_equal(gen_roles, test_data["GEN_ROLES"])

    total_count = get_fm_candidate_roles_total_count(upa, gen_roles)
    for role_label, count in total_count.items():
        assert role_label in test_data["TOTAL_COUNT"]
        assert count == test_data["TOTAL_COUNT"][role_label]


def test__get_fm_result():
    upa = load_upa_from_one2one_file("dataset/test_datasets/simple_dataset.txt")
    result, runtime = get_fast_miner_result(upa)
    assert result == {
        (1, 1, 0, 1): {"label": "P1,P2,P4", "original_count": 5, "total_count": 5},
        (0, 1, 0, 0): {"label": "P2", "original_count": 0, "total_count": 11},
        (0, 1, 0, 1): {"label": "P2,P4", "original_count": 0, "total_count": 8},
        (0, 0, 0, 1): {"label": "P4", "original_count": 2, "total_count": 10},
        (0, 1, 1, 0): {"label": "P2,P3", "original_count": 3, "total_count": 6},
        (0, 1, 1, 1): {"label": "P2,P3,P4", "original_count": 3, "total_count": 3},
    }


def test__basic_rmp__delta_factor_0():
    excepted_pa_matrix = {
        "R1": ["P2", "P4"],
        "R2": ["P2", "P3"],
        "R3": ["P1", "P2", "P4"],
        "R4": ["P4"],
    }
    excepted_ua_matrix = {
        "U1": ["R1", "R3"],
        "U2": ["R2"],
        "U3": ["R1", "R3"],
        "U4": ["R1", "R3"],
        "U5": ["R1", "R2"],
        "U6": ["R1", "R2"],
        "U7": ["R2"],
        "U8": ["R2"],
        "U9": ["R4"],
        "U10": ["R4"],
        "U11": ["R1", "R3"],
        "U12": ["R1", "R3"],
        "U13": ["R1", "R2"],
    }
    upa = load_upa_from_one2one_file("dataset/test_datasets/simple_dataset.txt")
    pa_matrix, ua_matrix = basic_rmp(upa, delta_factor=0)
    assert pa_matrix == excepted_pa_matrix
    assert ua_matrix == excepted_ua_matrix


def test__basic_rmp__delta_factor_1():
    excepted_pa_matrix = {
        "R1": ["P2", "P4"],
        "R2": ["P2", "P3"],
        "R3": ["P1", "P2", "P4"],
        "R4": ["P4"],
    }
    excepted_ua_matrix = {
        "U1": ["R1", "R3"],
        "U2": ["R2"],
        "U3": ["R1", "R3"],
        "U4": ["R1", "R3"],
        "U5": ["R1", "R2"],
        "U6": ["R1", "R2"],
        "U7": ["R2"],
        "U8": ["R2"],
        "U9": ["R4"],
        "U10": ["R4"],
        "U11": ["R1", "R3"],
        "U12": ["R1", "R3"],
        "U13": ["R1", "R2"],
    }
    upa = load_upa_from_one2one_file("dataset/test_datasets/simple_dataset.txt")
    pa_matrix, ua_matrix = basic_rmp(upa, delta_factor=1)
    assert pa_matrix == excepted_pa_matrix
    assert ua_matrix == excepted_ua_matrix


def test__basic_rmp__delta_factor_2():
    excepted_pa_matrix = {
        "R1": ["P2", "P4"],
        "R2": ["P2", "P3"],
        "R3": ["P1", "P2", "P4"],
    }
    excepted_ua_matrix = {
        "U1": ["R1", "R3"],
        "U2": ["R2"],
        "U3": ["R1", "R3"],
        "U4": ["R1", "R3"],
        "U5": ["R1", "R2"],
        "U6": ["R1", "R2"],
        "U7": ["R2"],
        "U8": ["R2"],
        "U11": ["R1", "R3"],
        "U12": ["R1", "R3"],
        "U13": ["R1", "R2"],
    }
    upa = load_upa_from_one2one_file("dataset/test_datasets/simple_dataset.txt")
    pa_matrix, ua_matrix = basic_rmp(upa, delta_factor=2)
    assert pa_matrix == excepted_pa_matrix
    assert ua_matrix == excepted_ua_matrix


def test__basic_rmp__identity_matrix__all_delta_factors():
    max_delta_factor = 5
    upa = load_upa_from_one2one_file("dataset/test_datasets/identity_matrix.txt")
    for delta_factor in range(max_delta_factor):
        pa, ua = basic_rmp(upa, delta_factor=delta_factor)
        assert len(pa) == max_delta_factor - delta_factor
        assert len(ua) == max_delta_factor - delta_factor
