import copy
from collections import defaultdict
from typing import Dict, List, Tuple

import numpy as np
from numpy import ndarray

from algorithms.utils_func import sort_dict_by_value
from dataset.upa_matrix import generate_upa_matrix, load_upa_from_one2one_file


class FastMinerException(Exception):
    pass


def get_role_label(role: np.ndarray) -> str:
    permissions = []
    for i, p in enumerate(role):
        if p:
            permissions.append(f"P{i+1}")
    return ",".join(permissions)


# region: Fast Miner Utils functions
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


def get_fm_candidate_roles_total_count(
    upa: np.ndarray, gen_roles: np.ndarray
) -> Dict[Tuple, int]:
    total_count: Dict[Tuple, int] = defaultdict(int)

    for r in gen_roles:
        for u in upa:
            if np.array_equal(np.bitwise_and(r, u), r):
                total_count[tuple(r)] += 1

    return sort_dict_by_value(total_count)


# endregion

# TODO: tests


def get_role_cover_area(upa: np.ndarray, role: np.ndarray) -> int:
    count = 0
    for row in upa:
        if all([r_i >= p for r_i, p in zip(row, role)]):
            for r_i, p in zip(row, role):
                if r_i == 1 and p == 1:
                    count += 1
    return count


def roles_subtraction(a: Tuple[int], b: Tuple[int]) -> tuple[int, ...]:
    result: List[int] = []
    for i in range(len(a)):
        if a[i] == 1 and b[i] == 1:
            result.append(0)
        else:
            result.append(a[i])
    return tuple(result)


def get_max_cover_role(upa: np.ndarray, list_of_roles: np.ndarray):
    # Get sorted list of roles by cover of area of UPA
    roles_by_cover_area = {
        tuple(role): get_role_cover_area(upa, role) for role in list_of_roles
    }
    roles_by_cover_area = sort_dict_by_value(roles_by_cover_area)

    # Get max cover role
    max_cover_role, covered_area = next(iter(roles_by_cover_area.items()))
    max_cover_role_array = np.array(max_cover_role)

    # Update UPA
    # Mark users that max_cover_role applied to them. Users permissions match the role marked by "2"
    _updated_upa = upa.copy()
    ua_dict = defaultdict(list)
    for i in range(_updated_upa.shape[0]):
        if np.all(
            (np.any(_updated_upa[i] == 1))
            & ((_updated_upa[i] >= 1) | (max_cover_role_array != 1))
        ):
            ua_dict[i + 1].append(max_cover_role)
            _updated_upa[i] = np.where(max_cover_role_array == 1, 2, _updated_upa[i])

    # Remove max_cover_role from potential roles list
    updated_list_of_roles = np.array(
        [
            role
            for role in list_of_roles
            if not np.array_equal(role, max_cover_role_array)
        ]
    )
    return max_cover_role, _updated_upa, updated_list_of_roles, ua_dict


if __name__ == "__main__":
    num_of_roles = 4
    upa = load_upa_from_one2one_file("dataset/test_datasets/simple_dataset.txt")
    # upa = load_upa_from_one2one_file("dataset/test_datasets/identity_matrix.txt")
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
    total_count = get_fm_candidate_roles_total_count(upa, gen_roles)
    print("Total count")
    print(total_count)

    print("RMP iteration")
    chosen_role, updated_upa, updated_roles, ua = get_max_cover_role(upa, gen_roles)
    print(chosen_role)
    print(updated_upa)
    print(updated_roles)
