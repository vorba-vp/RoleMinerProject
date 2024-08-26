from collections import defaultdict
from functools import lru_cache
from typing import Dict, Tuple

import numpy as np
from line_profiler import profile

from algorithms.utils_func import sort_dict_by_value
from dataset.upa_matrix import load_upa_from_one2one_file


class FastMinerException(Exception):
    pass


@lru_cache(maxsize=None)  # Cache with unlimited size
def get_role_label(role: tuple) -> str:
    return ",".join(f"P{i+1}" for i, p in enumerate(role) if p)


def get_role_label_with_cache(role: np.ndarray) -> str:
    role_tuple = tuple(role)
    return get_role_label(role_tuple)


# region: Fast Miner Utils functions
def get_init_roles(upa: np.ndarray) -> Tuple[np.ndarray | None, Dict]:
    num_of_users, num_of_permissions = upa.shape

    if num_of_users == 0 or num_of_permissions == 0:
        raise FastMinerException("UPA must have non-zero dimensions")

    roles_set = set()
    original_count: Dict[Tuple[int], int] = defaultdict(int)
    unique_roles = []

    for u in upa:
        u_label = tuple(u)
        original_count[u_label] += 1

        if u_label not in roles_set:
            roles_set.add(u_label)
            unique_roles.append(u)

    init_roles_set = np.array(unique_roles) if unique_roles else None

    return init_roles_set, dict(original_count)


def get_fm_gen_roles(init_roles: np.ndarray) -> np.ndarray | None:
    # Make a shallow copy of the input if mutation needs to be avoided.
    temp_init_roles = init_roles.copy()

    # Initialize generated roles and a set for uniqueness check.
    gen_roles = []
    roles_set = set()

    while len(temp_init_roles) > 0:
        candidate_role = temp_init_roles[0]
        temp_init_roles = temp_init_roles[1:]

        # Check and add the candidate role to gen_roles if not already present.
        role_tuple = tuple(candidate_role)
        if role_tuple not in roles_set:
            gen_roles.append(candidate_role)
            roles_set.add(role_tuple)

        # Generate new roles by intersecting candidate_role with other roles.
        new_roles = [
            np.bitwise_and(role, candidate_role)
            for role in temp_init_roles
            if (intersection := np.bitwise_and(role, candidate_role)).sum() > 0
            and tuple(intersection) not in roles_set
        ]

        # Add the new roles to gen_roles and roles_set.
        for new_role in new_roles:
            gen_roles.append(new_role)
            roles_set.add(tuple(new_role))

    return np.array(gen_roles) if gen_roles else None


def get_fm_candidate_roles_total_count(
    upa: np.ndarray, gen_roles: np.ndarray
) -> Dict[Tuple, int]:
    # Initialize the defaultdict to store counts
    total_count: Dict[Tuple, int] = defaultdict(int)

    # Iterate through each generated role
    for r in gen_roles:
        # Use broadcasting and vectorization to apply bitwise_and across all rows in upa
        mask = np.all(np.bitwise_and(upa, r) == r, axis=1)

        # Count the occurrences of rows that satisfy the condition
        total_count[tuple(r)] += np.sum(mask)

    return sort_dict_by_value(total_count)


# endregion

# TODO: tests


def get_role_cover_area(upa: np.ndarray, role: np.ndarray) -> tuple:
    # Convert role to a boolean mask
    role_mask = role == 1

    # Find valid rows where all elements are >= the corresponding role elements
    valid_rows = np.all(upa[:, role_mask] >= role[role_mask], axis=1)

    # Count the number of ones in valid rows for the masked columns
    count = np.sum(upa[valid_rows][:, role_mask] == 1)

    return tuple(role), count


def roles_subtraction(a: Tuple[int, ...], b: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(0 if x == 1 and y == 1 else x for x, y in zip(a, b))


def process_row(i, row, max_cover_role_array, max_cover_role) -> tuple:
    ua_dict_local = defaultdict(list)

    if np.all((np.any(row == 1)) & ((row >= 1) | (max_cover_role_array != 1))):
        ua_dict_local[i + 1].append(max_cover_role)
        updated_row = np.where(max_cover_role_array == 1, 2, row)
    else:
        updated_row = row

    return i, ua_dict_local, updated_row


@profile
def get_max_cover_role(upa: np.ndarray, list_of_roles: np.ndarray):
    # Step 1: Calculate the role cover areas sequentially
    result = [get_role_cover_area(upa, role) for role in list_of_roles]

    # Convert result into a dictionary and sort by cover area
    roles_by_cover_area = dict(result)
    roles_by_cover_area = sort_dict_by_value(roles_by_cover_area)

    # Step 2: Identify the role with the maximum cover area
    max_cover_role, covered_area = next(iter(roles_by_cover_area.items()))
    max_cover_role_array = np.array(max_cover_role)

    # Step 3: Update UPA in parallel
    _updated_upa = upa.copy()  # Copy the UPA array only once

    # Process each row of UPA sequentially
    results = [
        process_row(i, _updated_upa[i], max_cover_role_array, max_cover_role)
        for i in range(_updated_upa.shape[0])
    ]

    # Step 4: Aggregate results
    ua_dict: dict[tuple, list] = defaultdict(list)
    for i, local_dict, updated_row in results:
        ua_dict.update(local_dict)  # Update the user-role assignments
        _updated_upa[i] = updated_row  # Update UPA with processed rows

    # Step 5: Filter out the max cover role from the list of roles
    # Use boolean indexing to filter out the roles without copying the entire array
    mask = ~np.all(list_of_roles == max_cover_role_array, axis=1)
    updated_list_of_roles = list_of_roles[mask]

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
