import random
import re
import time

import numpy as np


class UpaMatrixBuilder:
    @staticmethod
    def load_from_one2one_file(filename: str) -> np.ndarray:
        num_of_users, num_of_permissions = 0, 0

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

    @staticmethod
    def generate_matrix(
        num_of_roles: int,
        num_of_users: int,
        num_of_permissions: int,
        max_roles_per_user: int,
        max_permissions_per_role: int,
    ) -> np.ndarray:
        roles = UpaMatrixBuilder._generate_pa_matrix(
            num_of_roles, num_of_permissions, max_permissions_per_role
        )

        for idx, role in enumerate(roles):
            print(f"Role {idx + 1}: {role}")

    @staticmethod
    def _generate_pa_matrix(
        num_of_roles: int, num_of_permissions: int, max_permissions_per_role: int
    ) -> np.ndarray:
        roles = np.zeros((num_of_roles, num_of_permissions), dtype=int)
        for r in range(num_of_roles):
            nrt = random.randint(1, max_permissions_per_role)
            role = np.zeros(num_of_permissions, dtype=int)

            random_positions = random.sample(range(num_of_permissions), nrt)
            for pos in random_positions:
                roles[r, pos] = 1
        return roles


if __name__ == "__main__":
    start_time = time.time()

    # matrix = UpaMatrixBuilder.load_from_one2one_file("real_datasets/healthcare.txt")
    # print(matrix)
    UpaMatrixBuilder.generate_matrix(5, 12, 7, 1, 4)

    elapsed_time = time.time() - start_time
    print(f"--- {elapsed_time} seconds ---")
