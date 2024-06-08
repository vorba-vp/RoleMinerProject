import numpy as np

from algorithms.miner_utils import (
    get_candidate_roles_total_count,
    get_fm_gen_roles,
    get_init_roles,
)
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

    total_count = get_candidate_roles_total_count(upa, gen_roles)
    for role_label, count in total_count.items():
        assert role_label in test_data["TOTAL_COUNT"]
        assert count == test_data["TOTAL_COUNT"][role_label]
