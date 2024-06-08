import copy
from collections import defaultdict
from typing import Dict, Tuple

import numpy as np

from dataset.upa_matrix import generate_upa_matrix, load_upa_from_one2one_file


class FastMinerException(Exception):
    pass


def get_init_roles(upa: np.ndarray) -> Tuple[np.ndarray | None, Dict]:
    num_of_users, num_of_permissions = upa.shape
    if not num_of_users or not num_of_permissions:
        raise FastMinerException("UPA must have non-zero dimensions")
    init_roles_set: np.ndarray | None = None
    roles_set = set()
    original_count: Dict[Tuple, int] = defaultdict(int)
    for u in upa:
        u_label = tuple(u)
        original_count[u_label] += 1
        if u_label in roles_set:
            continue
        else:
            roles_set.add(u_label)
            init_roles_set = (
                np.vstack((init_roles_set, u)) if init_roles_set is not None else u
            )
    return init_roles_set, dict(original_count)


def get_fm_gen_roles(init_roles: np.ndarray) -> np.ndarray | None:
    temp_init_roles = copy.deepcopy(init_roles)
    gen_roles: np.ndarray | None = None
    roles_set = set()
    while len(temp_init_roles) > 0:
        candidate_role = temp_init_roles[0]
        temp_init_roles = temp_init_roles[1:]
        if tuple(candidate_role) not in roles_set:
            gen_roles = (
                np.vstack((gen_roles, candidate_role))
                if gen_roles is not None
                else candidate_role
            )
            roles_set.add(tuple(candidate_role))
        for role in temp_init_roles:
            intersection = np.bitwise_and(role, candidate_role)
            if intersection.sum() > 0 and tuple(intersection) not in roles_set:
                roles_set.add(tuple(intersection))
                gen_roles = np.vstack((gen_roles, intersection))
    return gen_roles


def get_candidate_roles_total_count(
    upa: np.ndarray, gen_roles: np.ndarray
) -> Dict[Tuple, int]:
    total_count: Dict[Tuple, int] = defaultdict(int)

    for r in gen_roles:
        for u in upa:
            # print(f"TEST: {}")
            if np.array_equal(np.bitwise_and(r, u), r):
                total_count[tuple(r)] += 1

    return dict(total_count)


# TODO: tests
# TODO: total count


if __name__ == "__main__":
    num_of_roles = 4
    # upa = load_upa_from_one2one_file("dataset/test_datasets/simple_dataset.txt")
    upa = load_upa_from_one2one_file("dataset/test_datasets/identity_matrix.txt")
    # upa = load_upa_from_one2one_file("dataset/real_datasets/americas_large.txt")
    print("UPA")
    print(upa)
    print("INIT_ROLES")
    init_roles, original_count = get_init_roles(upa)
    print(init_roles)
    print("Original Count")
    print(original_count)
    assert init_roles is not None
    # assert len(init_roles) == num_of_roles
    gen_roles: np.ndarray = get_fm_gen_roles(init_roles)
    print("GEN_ROLES")
    print(gen_roles)
    total_count = get_candidate_roles_total_count(upa, gen_roles)
    print("Total count")
    print(total_count)
