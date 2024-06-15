import time
from typing import Dict, Tuple

import numpy as np

from algorithms.miner_utils import (
    get_candidate_roles_total_count,
    get_fm_gen_roles,
    get_init_roles,
)


def get_role_label(role: np.ndarray) -> str:
    permissions = []
    for i, p in enumerate(role):
        if p:
            permissions.append(f"P{i+1}")
    return ",".join(permissions)


def get_fast_miner_result(upa: np.ndarray) -> Tuple[Dict, float]:
    start_time = time.time()
    result = {}
    init_roles, original_count = get_init_roles(upa)
    gen_roles = get_fm_gen_roles(init_roles)
    if gen_roles is not None:
        total_count = get_candidate_roles_total_count(upa, gen_roles)

        for candidate in gen_roles:
            result[tuple(candidate)] = {
                "label": get_role_label(candidate),
                "original_count": original_count.get(tuple(candidate), 0),
                "total_count": total_count[tuple(candidate)],
            }

    return result, time.time() - start_time


if __name__ == "__main__":
    from dataset.upa_matrix import load_upa_from_one2one_file

    upa = load_upa_from_one2one_file("dataset/test_datasets/simple_dataset.txt")
    result, runtime = get_fast_miner_result(upa)
    for k, v in result.items():
        print(f"{k}: {v}")
    print(f"Time in seconds: {runtime}")