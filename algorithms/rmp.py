import os
from collections import defaultdict

import numpy as np

from algorithms.fast_miner import get_fast_miner_result
from algorithms.miner_utils import get_max_cover_role, get_role_label


def basic_rmp(upa: np.ndarray, delta_factor: int = 0):
    gen_roles, _ = get_fast_miner_result(upa)
    gen_roles_list = np.array([r for r in gen_roles.keys()])

    updated_upa = upa.copy()
    pa_list = []
    ua_dict = defaultdict(list)
    while np.sum(updated_upa == 1) > delta_factor:
        role, updated_upa, gen_roles_list, users_list = get_max_cover_role(
            updated_upa, gen_roles_list
        )
        pa_list.append(get_role_label(role))
        for k, v in users_list.items():
            ua_dict[k].extend([get_role_label(r) for r in v])
    sorted_ua_dict = dict(sorted(ua_dict.items()))
    pa_matrix = {}
    roles_label_mapping = {}
    for i, r in enumerate(pa_list):
        role_label = f"R{i+1}"
        pa_matrix[role_label] = r.split(",")
        roles_label_mapping[r] = role_label
    ua_matrix = {}
    for k, v in sorted_ua_dict.items():
        ua_matrix[f"U{k}"] = [roles_label_mapping[r] for r in v]
    return pa_matrix, ua_matrix


if __name__ == "__main__":
    import time

    from dataset.upa_matrix import load_upa_from_one2one_file

    datasets_dir = "dataset/real_datasets"
    datasets_list = os.listdir(datasets_dir)
    datasets_list.reverse()
    for dataset in datasets_list:
        start_time = time.time()
        upa = load_upa_from_one2one_file(f"{datasets_dir}/{dataset}")
        basic_rmp(upa)
        print(f"{dataset}: --- {time.time() - start_time} seconds ---")

    # pa, ua = basic_rmp(upa, delta_factor=1)
    # print("UPA matrix")
    # print(upa)
    # print("PA matrix")
    # print(pa)
    # print("UA matrix")
    # print(ua)
    #
    # print("--- %s seconds ---" % (time.time() - start_time))
