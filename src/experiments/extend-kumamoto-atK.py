from src.tour.preprocessing.read_cikm16 import (
    read_poi,
    read_traj,
)
from src.tour.util.utility import calc_poi_info
from src.tour.types.datatype import City
from src.tour.util.evaluate import calc_F1, calc_pairsF1
from src.tour.factorize.factorize import gen_poi_logtransmat
from src.tour.solver.pop import find_by_popularity_at_k
from src.tour.solver.ilp import find_ILP_at_K
import sys
import random
import numpy as np

random.seed(0)
np.random.seed(0)


def main(city: City, BIN_CLUSTER: int = 5) -> None:
    print(f"{city}")

    # traj.
    traj_all, trajid_set_all, traj_dict = read_traj(city, delimiter=",")

    # POI
    poi_all, _ = read_poi(city, delimiter=",")

    # at K
    K = 8
    list_th = [5]
    recdict = dict()
    count = 1
    for i in range(len(trajid_set_all)):
        tid = trajid_set_all[i]
        te = traj_dict[tid]

        # trajectory is too short OR loop
        if len(te) < 3 or len(set(te)) < len(te) or len(te) > 10:
            continue

        trajid_list_train = trajid_set_all[:i] + trajid_set_all[i + 1 :]
        poi_info = calc_poi_info(trajid_list_train, traj_all, poi_all)

        # start/end is not in training set
        if not (te[0] in poi_info.index and te[-1] in poi_info.index):
            continue
        print(tid, "|", te, "#%d ->" % count)
        count += 1
        sys.stdout.flush()

        # recommend
        rec1 = find_by_popularity_at_k(poi_info.copy(), te, k=K)
        recdict[tid] = {"REAL": te, "Pop@K": None}
        print(" " * 10, "Pop", rec1[0])
        recdict[tid]["Pop@K"] = rec1[0]
        for th in list_th:
            recdict[tid][f"Pop@{th}-rank"] = -1
            if te in rec1[:th]:
                recdict[tid][f"Pop@{th}-rank"] = rec1.index(te)

        # recommendation leveraging transition probabilities
        poi_logtransmat = gen_poi_logtransmat(
            trajid_list_train, traj_dict, poi_info, BIN_CLUSTER=BIN_CLUSTER
        )
        edges = poi_logtransmat.copy()
        solutions = []
        prevsol = []
        for k in range(K):
            flag, tran_ilp_at_k = find_ILP_at_K(
                poi_info.copy(), edges.copy(), te[0], te[-1], len(te), edgs=prevsol
            )
            if not flag:
                break
            if k == 0:
                print(" " * 10, f"ILP({k}):", tran_ilp_at_k)
            edge = []
            for j in range(len(tran_ilp_at_k) - 1):
                edge.append((tran_ilp_at_k[j], tran_ilp_at_k[j + 1]))
            prevsol.append(edge)
            solutions.append(tran_ilp_at_k)

        if len(solutions) == K:
            recdict[tid]["ILP@K"] = solutions[0]
            for th in list_th:
                recdict[tid][f"ILP@{th}-rank"] = -1
                if te in solutions[:th]:
                    recdict[tid][f"ILP@{th}-rank"] = solutions.index(te)
        else:
            del recdict[tid]

    # F1 / pairs-F1
    F11_mpK = []
    pF11_mpK = []
    F11_popK = []
    pF11_popK = []
    for tid in sorted(recdict.keys()):
        real = recdict[tid]["REAL"]
        popK = recdict[tid]["ILP@K"]
        F11_mpK.append(calc_F1(real, popK))
        pF11_mpK.append(calc_pairsF1(real, popK))
        popK = recdict[tid]["Pop@K"]
        F11_popK.append(calc_F1(real, popK))
        pF11_popK.append(calc_pairsF1(real, popK))

    # Ranking measure
    # for th in list_th:
    th = 5
    M = len(recdict)
    mean_rank_th_mp = 0.0
    mean_rank_th_pop = 0.0
    for tid in sorted(recdict.keys()):
        # MP@K
        rank = recdict[tid][f"ILP@{th}-rank"]
        if rank >= 0:
            mean_rank_th_mp += 1.0 / (rank + 1)
        else:
            mean_rank_th_mp += 0

        # POP@K
        rank = recdict[tid][f"Pop@{th}-rank"]
        if rank >= 0:
            mean_rank_th_pop += 1.0 / (rank + 1)
        else:
            mean_rank_th_pop += 0
    mean_rank_th_pop /= M
    mean_rank_th_mp /= M

    print(
        "Pop: F1 (%.3f, %.3f), pairsF1 (%.3f, %.3f), MRR-Pop@K %.3f"
        % (
            np.mean(F11_popK),
            np.std(F11_popK),
            np.mean(pF11_popK),
            np.std(pF11_popK),
            mean_rank_th_pop,
        )
    )
    print(
        "ILP: F1 (%.3f, %.3f), pairsF1 (%.3f, %.3f), MRR-ILP@K %.3f"
        % (
            np.mean(F11_mpK),
            np.std(F11_mpK),
            np.mean(pF11_mpK),
            np.std(pF11_mpK),
            mean_rank_th_mp,
        )
    )

    # write to file
    fn_path = city.get_fn_log()
    print(fn_path)
    with open(fn_path, "w") as f:
        f.write("method,F1m,F1s,pF1m,pF1s,MRR@5\n")
        f.write(
            f"Pop,{np.mean(F11_popK):>.3f},{np.std(F11_popK):>.3f},{np.mean(pF11_popK):>.3f},{np.std(pF11_popK):>.3f},{mean_rank_th_pop:>.3f}\n"
        )
        f.write(
            f"ILP,{np.mean(F11_mpK):>.3f},{np.std(F11_mpK):>.3f},{np.mean(pF11_mpK):>.3f},{np.std(pF11_mpK):>.3f},{mean_rank_th_mp:>.3f}\n"
        )


if __name__ == "__main__":
    city = City("kumamoto", config_fn="config/extended/kumamoto-atK.json")
    main(city)
