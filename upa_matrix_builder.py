import re
import time

import numpy as np


class UpaMatrixBuilder:
    @classmethod
    def load_from_one2one_file(cls, filename: str) -> np.ndarray:
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

        num_of_users = max(user_set)
        num_of_permissions = max(permission_set)

        upa_matrix = np.zeros((num_of_users, num_of_permissions))

        with open(filename, "r") as file:
            for line in file:
                user_num, permission_num = map(
                    int, re.sub(r"\s+", " ", line.strip()).split(" ")
                )
                upa_matrix[user_num - 1][permission_num - 1] = 1

        return upa_matrix


if __name__ == "__main__":
    start_time = time.time()

    matrix = UpaMatrixBuilder.load_from_one2one_file("real_datasets/healthcare.txt")
    print(matrix)

    elapsed_time = time.time() - start_time
    print(f"--- {elapsed_time} seconds ---")
