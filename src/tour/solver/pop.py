import pandas as pd
import numpy as np
from typing import List
from itertools import combinations


def find_by_popularity(poi_info: pd.DataFrame, te: List[int]) -> List[int]:
    # POI popularity based ranking
    poi_info.sort_values(by="popularity", ascending=False, inplace=True)
    ranks1 = poi_info.index.tolist()
    rank_pop = (
        [te[0]]
        + [x for x in ranks1 if x not in {te[0], te[-1]}][: len(te) - 2]
        + [te[-1]]
    )
    return rank_pop


def find_by_popularity_at_k(
    poi_info: pd.DataFrame, te: List[int], k: int = 1
) -> List[List[int]]:
    # POI popularity based ranking
    poi_info.sort_values(by="popularity", ascending=False, inplace=True)

    # all POI and popularity
    M = poi_info.shape[0]
    indices = poi_info.index.tolist()[: max(min(2 * k, M), len(te) * 2)]
    values = poi_info.popularity.values.tolist()[: max(min(2 * k, M), len(te) * 2)]

    # POI and popularity excluding `start` and `goal`
    indices_rm = [x for x in indices if x not in {te[0], te[-1]}]
    values_rm = [x for (i, x) in enumerate(values) if indices[i] not in {te[0], te[-1]}]
    sums_dict = {}
    for comb in combinations(range(len(indices_rm)), len(te) - 2):
        sum_value = sum(values_rm[i] for i in comb)
        sums_dict[sum_value] = comb

    # get `k` combinations (with higher popularity values)
    sorted_sums = sorted(sums_dict.keys(), reverse=True)
    result_index = [sums_dict[sorted_sums[i]] for i in range(min(len(sorted_sums), k))]
    result_tour = []
    for idx in result_index:
        tour = [te[0]] + [indices_rm[i] for i in idx] + [te[-1]]
        # print(idx, tour)
        assert len(tour) == len(set(tour))
        result_tour.append(tour)

    return result_tour
