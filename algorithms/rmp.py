import os
import time
from collections import defaultdict

import numpy as np
from line_profiler import profile

from algorithms.fast_miner import get_fast_miner_result_with_metadata, get_fast_miner_result
from algorithms.miner_utils import get_max_cover_role, get_role_label_with_cache


@profile
def basic_rmp(upa: np.ndarray, delta_factor: int = 0):
    start_time = time.time()
    gen_roles_list = get_fast_miner_result(upa)
    print()
    print(f"\tFastMiner calc time: {time.time() - start_time} seconds")

    updated_upa = upa.copy()
    pa_list = []
    ua_dict = defaultdict(list)

    # Cache roles_label_mapping within the loop to avoid re-computation
    roles_label_mapping = {}

    # Main loop
    roles_cover_map: dict[tuple, int] = {}
    while np.sum(updated_upa == 1) > delta_factor:
        role, updated_upa, gen_roles_list, users_list, roles_cover_map = (
            get_max_cover_role(
                updated_upa, gen_roles_list, roles_cover_map, delta_factor
            )
        )
        role_label = get_role_label_with_cache(role)

        # Add the role to pa_list and update mapping
        pa_list.append(role_label)

        # Ensure roles_label_mapping is populated only once per role
        if role_label not in roles_label_mapping:
            roles_label_mapping[role_label] = f"R{len(pa_list)}"

        # Update ua_dict efficiently with batched list extensions
        for k, v in users_list.items():
            ua_dict[k].extend([get_role_label_with_cache(r) for r in v])

    # Create pa_matrix from pa_list and roles_label_mapping
    pa_matrix = {roles_label_mapping[r]: r.split(",") for r in pa_list}

    # Sort ua_dict once and create ua_matrix
    ua_matrix = {
        f"U{k}": [roles_label_mapping[r] for r in v] for k, v in sorted(ua_dict.items())
    }
    return pa_matrix, ua_matrix


if __name__ == "__main__":
    import time

    from dataset.upa_matrix import load_upa_from_one2one_file

    datasets_dir = "dataset/real_datasets"
    datasets_list = os.listdir(datasets_dir)
    # datasets_list.reverse()
    for dataset in datasets_list:
        print()
        print(f"Dataset: {dataset}")
        start_time = time.time()
        upa = load_upa_from_one2one_file(f"{datasets_dir}/{dataset}")
        basic_rmp(upa)
        print(f"\tTotal time: {time.time() - start_time} seconds")
        print()

    # pa, ua = basic_rmp(upa, delta_factor=1)
    # print("UPA matrix")
    # print(upa)
    # print("PA matrix")
    # print(pa)
    # print("UA matrix")
    # print(ua)
    #
    # print("--- %s seconds ---" % (time.time() - start_time))
