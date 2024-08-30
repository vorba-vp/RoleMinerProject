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
    # Use a set to track unique roles as tuples for fast lookups.
    roles_set = set()
    gen_roles = []

    # Iterate over the roles in the initial array.
    for i, candidate_role in enumerate(init_roles):
        role_tuple = tuple(candidate_role)
        if role_tuple not in roles_set:
            gen_roles.append(candidate_role)
            roles_set.add(role_tuple)

        # Calculate the intersection (bitwise AND) of the candidate role with the remaining roles.
        intersections = np.bitwise_and(init_roles[i + 1:], candidate_role)

        # Filter out zero-sum intersections and duplicates.
        non_zero_intersections = intersections[np.any(intersections, axis=1)]
        new_roles = [role for role in non_zero_intersections if tuple(role) not in roles_set]

        # Add the new unique roles to the generated roles list and the roles_set.
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


def get_role_cover_area(upa: np.ndarray, role: np.ndarray) -> tuple[tuple, int]:
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

    # Determine if the row should be updated
    if np.any(row == 1) and np.all((row >= 1) | (max_cover_role_array != 1)):
        # Update ua_dict_local and the row
        ua_dict_local[i + 1].append(max_cover_role)
        updated_row = np.where(max_cover_role_array == 1, 2, row)
    else:
        updated_row = row

    return i, ua_dict_local, updated_row


@profile
def get_max_cover_role(
    upa: np.ndarray,
    list_of_roles: np.ndarray,
    prev_covered_areas: dict,
    delta_factor: int = 0,
):
    covered_area = 0
    max_cover_role = None
    max_area = np.sum(upa)

    for role in list_of_roles:
        role_key = tuple(role)

        # Skip roles that have already been processed with worse or equal coverage
        if (
            role_key in prev_covered_areas
            and prev_covered_areas[role_key] <= covered_area
        ):
            continue

        # Compute the cover area for the current role
        _role, _covered_area = get_role_cover_area(upa, role)

        # Store the covered area for this role
        prev_covered_areas[role_key] = _covered_area

        # Update the max cover role if the current one is better
        if _covered_area > covered_area:
            max_cover_role = _role
            covered_area = _covered_area

        # Early exit if the current covered area is sufficient
        if covered_area >= max_area - delta_factor:
            break

    # Convert max_cover_role to a numpy array
    max_cover_role_array = np.array(max_cover_role)

    # Update UPA without parallel processing
    _updated_upa = upa.copy()

    ua_dict: dict[tuple, list] = defaultdict(list)
    for i in range(_updated_upa.shape[0]):
        # Process each row and update UPA
        local_dict, updated_row = process_row(
            i, _updated_upa[i], max_cover_role_array, max_cover_role
        )[1:]
        ua_dict.update(local_dict)
        _updated_upa[i] = updated_row

    # Filter out the max cover role from the list of roles
    mask = ~np.all((list_of_roles >= max_cover_role_array) & (list_of_roles == max_cover_role_array), axis=1)
    updated_list_of_roles = list_of_roles[mask]

    return (
        max_cover_role,
        _updated_upa,
        updated_list_of_roles,
        ua_dict,
        prev_covered_areas,
    )


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
