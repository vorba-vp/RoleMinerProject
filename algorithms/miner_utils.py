import numpy as np

from dataset.upa_matrix import generate_upa_matrix


def get_init_roles(upa: np.ndarray) -> np.ndarray:
    num_of_users, num_of_permissions = upa.shape
    init_roles_set = np.zeros(num_of_permissions, dtype=int)
    roles_set = set()
    for u in upa:
        if tuple(u) in roles_set:
            continue
        else:
            roles_set.add(tuple(u))
            init_roles_set = np.vstack((init_roles_set, u))
    return init_roles_set[1:]


if __name__ == "__main__":
    upa = generate_upa_matrix(
        num_of_roles=5,
        num_of_users=15,
        num_of_permissions=7,
        max_permissions_per_role=4,
        max_roles_per_user=1,
    )
    print("UPA")
    print(upa)
    print("INIT_ROLES")
    init_roles = get_init_roles(upa)
    print(init_roles)
