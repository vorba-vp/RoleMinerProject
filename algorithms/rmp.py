import numpy as np

from algorithms.fast_miner import get_fast_miner_result
from algorithms.miner_utils import get_max_cover_role, get_role_label


def basic_rmp(upa: np.ndarray, delta_factor: int = 0):
    gen_roles, _ = get_fast_miner_result(upa)
    gen_roles_list = np.array([r for r in gen_roles.keys()])
    updated_upa = upa.copy()
    final_roles_list = []
    while np.sum(updated_upa == 1) > delta_factor:
        role, updated_upa, gen_roles_list = get_max_cover_role(
            updated_upa, gen_roles_list
        )
        final_roles_list.append(get_role_label(role))
    return final_roles_list


if __name__ == "__main__":
    import time

    from dataset.upa_matrix import load_upa_from_one2one_file

    start_time = time.time()
    upa = load_upa_from_one2one_file("dataset/test_datasets/simple_dataset.txt")
    result = basic_rmp(upa)
    print("Result")
    for r in result:
        print(r)
    print("--- %s seconds ---" % (time.time() - start_time))
