from typing import Dict, Tuple


def sort_dict_by_value(dict_to_sort: Dict[Tuple, int]) -> Dict[Tuple, int]:
    return dict(sorted(dict_to_sort.items(), key=lambda item: item[1], reverse=True))
