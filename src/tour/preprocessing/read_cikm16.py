from ..types.datatype import City
from ..util.utility import extract_traj
from ..preprocessing.distance import compute_poi_distmat
from typing import Tuple, Set, Dict, List
import pandas as pd


def read_poi(city: City, delimiter: str = ";") -> Tuple[pd.DataFrame, pd.DataFrame]:
    fn = city.get_fn_poi()
    df = pd.read_csv(fn, delimiter=delimiter)
    df.set_index("poiID", inplace=True)
    poi_distmat = compute_poi_distmat(df)
    return df, poi_distmat


def read_traj(
    city: City, delimiter: str = ";"
) -> Tuple[pd.DataFrame, Set[int], Dict[int, List[int]]]:
    fn = city.get_fn_traj()
    df = pd.read_csv(fn, delimiter=delimiter)

    # pre-processing
    trajid_set_all = sorted(df["trajID"].unique().tolist())
    traj_dict = dict()
    for trajid in trajid_set_all:
        traj = extract_traj(trajid, df)
        assert trajid not in traj_dict
        traj_dict[trajid] = traj

    return df, trajid_set_all, traj_dict


def extract_query_from_traj(
    traj_all: pd.DataFrame, traj_dict: Dict[int, List[int]], flag_printstat: bool = True
) -> Dict[int, Tuple[int, int, int]]:
    """
    Extract query `(start, end, length) --> qid'
    """
    QUERY_ID_DICT = dict()
    keys = [
        (traj_dict[x][0], traj_dict[x][-1], len(traj_dict[x]))
        for x in sorted(traj_dict.keys())
        if len(traj_dict[x]) > 2
    ]
    cnt = 0
    for key in keys:
        if key not in QUERY_ID_DICT:  # (start, end, length) --> qid
            QUERY_ID_DICT[key] = cnt
            cnt += 1

    if flag_printstat:
        print("#traj in total:", traj_all.shape[0])
        print(
            "#traj (length > 2):",
            traj_all[traj_all["trajLen"] > 2]["trajID"].unique().shape[0],
        )
        print("#query tuple:", len(QUERY_ID_DICT))

    WHOLE_SET = traj_all[traj_all["trajLen"] > 2]["trajID"].unique()
    return QUERY_ID_DICT, WHOLE_SET
