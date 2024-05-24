import configparser
import random
import re
import time

import numpy as np

config = configparser.ConfigParser()
config.read("config.ini")

MIN_PERMISSIONS_PER_ROLE = config.getint("permissions", "min_per_role")


def load_upa_from_one2one_file(filename: str) -> np.ndarray:

    # Using a set to hold unique user and permission numbers for calculating the size of the matrix
    user_set, permission_set = set(), set()

    with open(filename, "r") as file:
        for line in file:
            user_num, permission_num = map(
                int, re.sub(r"\s+", " ", line.strip()).split(" ")
            )
            user_set.add(user_num)
            permission_set.add(permission_num)
    if not user_set or not permission_set:
        return np.zeros((0, 0), dtype=int)
    num_of_users = max(user_set)
    num_of_permissions = max(permission_set)

    upa_matrix = np.zeros((num_of_users, num_of_permissions), dtype=int)

    with open(filename, "r") as file:
        for line in file:
            user_num, permission_num = map(
                int, re.sub(r"\s+", " ", line.strip()).split(" ")
            )
            upa_matrix[user_num - 1][permission_num - 1] = 1

    return upa_matrix


def generate_upa_matrix(
    *,
    num_of_roles: int,
    num_of_users: int,
    num_of_permissions: int,
    max_roles_per_user: int,
    max_permissions_per_role: int,
) -> np.ndarray:
    roles = generate_pa_matrix(
        num_of_roles=num_of_roles,
        num_of_permissions=num_of_permissions,
        max_permissions_per_role=max_permissions_per_role,
    )

    users = np.zeros((num_of_users, num_of_permissions), dtype=int)
    for u in range(num_of_users):
        nrl = random.randint(1, max_roles_per_user)
        random_roles = random.sample(range(num_of_roles), nrl)
        for r in random_roles:
            users[u] = np.logical_or(users[u], roles[r])

    return users


def generate_pa_matrix(
    *, num_of_roles: int, num_of_permissions: int, max_permissions_per_role: int
) -> np.ndarray:
    roles = np.zeros((num_of_roles, num_of_permissions), dtype=int)
    for r in range(num_of_roles):
        nrt = random.randint(MIN_PERMISSIONS_PER_ROLE, max_permissions_per_role)
        role = np.zeros(num_of_permissions, dtype=int)

        random_positions = random.sample(range(num_of_permissions), nrt)
        for pos in random_positions:
            roles[r, pos] = 1
    return roles


if __name__ == "__main__":
    start_time = time.time()

    # matrix = UpaMatrixBuilder.load_from_one2one_file("real_datasets/healthcare.txt")
    # print(matrix)
    matrix = generate_upa_matrix(
        num_of_roles=5,
        num_of_users=12,
        num_of_permissions=7,
        max_roles_per_user=1,
        max_permissions_per_role=3,
    )
    print(matrix)

    elapsed_time = time.time() - start_time
    print(f"--- {elapsed_time} seconds ---")
