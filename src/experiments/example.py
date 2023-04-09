from src.tour.preprocessing.read_cikm16 import (
    read_poi,
    read_traj,
    extract_query_from_traj,
)
from src.tour.preprocessing.stat import compute_traj_stat
from src.tour.util.utility import calc_poi_info
from src.tour.util.evaluate import calc_F1, calc_pairsF1
from src.tour.factorize.factorize import gen_poi_logtransmat
from src.tour.types.datatype import City
from src.tour.solver.ilp import find_ILP
from src.tour.solver.pop import find_by_popularity
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

random.seed(0)
np.random.seed(0)


def main(city: City, BIN_CLUSTER: int = 5) -> None:
    print(f"{city}")

    # traj.
    traj_all, trajid_set_all, traj_dict = read_traj(city, delimiter=",")
    query_id_dict, whole_set = extract_query_from_traj(traj_all, traj_dict)
    print(traj_all.head())
    print(whole_set)

    df_stat = compute_traj_stat(city, traj_all)
    print(df_stat)
    # basic_stat_figures(city, traj_all)

    # POI
    poi_all, poi_distmat = read_poi(city, delimiter=",")
    poi_info_all = calc_poi_info(trajid_set_all, traj_all, poi_all)
    print(poi_all.head())
    print(poi_distmat.head())
    print(poi_info_all.head())

    recdict = dict()
    count = 1
    for i in range(len(trajid_set_all)):
        tid = trajid_set_all[i]
        te = traj_dict[tid]

        # trajectory is too short or too long
        if len(te) < 3 or len(set(te)) < len(te) or len(te) > 10:
            continue

        trajid_list_train = trajid_set_all[:i] + trajid_set_all[i + 1 :]

        poi_info = calc_poi_info(trajid_list_train, traj_all, poi_all)

        # start/end is not in training set
        if not (te[0] in poi_info.index and te[-1] in poi_info.index):
            continue

        print(te, "#%d ->" % count)
        count += 1
        sys.stdout.flush()

        # recommendation leveraging popularity
        rank_pop = find_by_popularity(poi_info.copy(), te)

        # recommendation leveraging transition probabilities
        poi_logtransmat = gen_poi_logtransmat(
            trajid_list_train, traj_dict, poi_info, BIN_CLUSTER=BIN_CLUSTER
        )
        edges = poi_logtransmat.copy()

        tran_ilp = find_ILP(poi_info.copy(), edges.copy(), te[0], te[-1], len(te))

        recdict[tid] = {
            "REAL": te,
            "REC_POP": rank_pop,
            "REC_ILP": tran_ilp,
        }
        print(" " * 10, "Rank POP:", rank_pop)
        print(" " * 10, "Tran ILP:", tran_ilp)
        sys.stdout.flush()

    F11_rank = []
    F12_tran = []
    pF11_rank = []
    pF12_tran = []
    for tid in sorted(recdict.keys()):
        real = recdict[tid]["REAL"]
        pop = recdict[tid]["REC_POP"]
        ilp = recdict[tid]["REC_ILP"]
        F11_rank.append(calc_F1(real, pop))
        F12_tran.append(calc_F1(real, ilp))
        pF11_rank.append(calc_pairsF1(real, pop))
        pF12_tran.append(calc_pairsF1(real, ilp))
    print(
        "Rank POP: F1 (%.3f, %.3f), pairsF1 (%.3f, %.3f)"
        % (np.mean(F11_rank), np.std(F11_rank), np.mean(pF11_rank), np.std(pF11_rank))
    )
    print(
        "Tran ILP: F1 (%.3f, %.3f), pairsF1 (%.3f, %.3f)"
        % (np.mean(F12_tran), np.std(F12_tran), np.mean(pF12_tran), np.std(pF12_tran))
    )

    # write to file
    fn_path = city.get_fn_log()
    with open(fn_path, "w") as f:
        f.write("method,F1m,F1s,pF1m,pF1s\n")
        f.write(
            f"POP,{np.mean(F11_rank):>.3f},{np.std(F11_rank):>.3f},{np.mean(pF11_rank):>.3f},{np.std(pF11_rank):>.3f}\n"
        )
        f.write(
            f"ILP,{np.mean(F12_tran):>.3f},{np.std(F12_tran):>.3f},{np.mean(pF12_tran):>.3f},{np.std(pF12_tran):>.3f}\n"
        )


if __name__ == "__main__":
    # Exp (Rep. paper)
    city0 = City("Osak", config_fn="./config/osak.json")
    city1 = City("Glas", config_fn="./config/glas.json")
    for city in [city0, city1]:
        print(city)
        main(city)
