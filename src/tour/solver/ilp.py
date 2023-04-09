import pandas as pd
import numpy as np
import pulp
from typing import List


def find_ILP(
    V: pd.DataFrame,
    E: pd.DataFrame,
    ps: int,
    pe: int,
    L: int,
    withNodeWeight=False,
    alpha=0.5,
    n_jobs: int = 4,
) -> List[int]:
    assert isinstance(V, pd.DataFrame)
    assert isinstance(E, pd.DataFrame)
    assert ps in V.index
    assert pe in V.index
    assert 2 < L <= V.index.shape[0]
    if withNodeWeight == True:
        assert 0 < alpha < 1
    beta = 1 - alpha

    p0 = str(ps)
    pN = str(pe)
    N = V.index.shape[0]

    # REF: pythonhosted.org/PuLP/index.html
    pois = [str(p) for p in V.index]  # create a string list for each POI
    pb = pulp.LpProblem("MostLikelyTraj", pulp.LpMaximize)  # create problem
    # visit_i_j = 1 means POI i and j are visited in sequence
    visit_vars = pulp.LpVariable.dicts("visit", (pois, pois), 0, 1, pulp.LpInteger)
    # a dictionary contains all dummy variables
    dummy_vars = pulp.LpVariable.dicts(
        "u", [x for x in pois if x != p0], 2, N, pulp.LpInteger
    )

    # add objective
    objlist = []
    if withNodeWeight == True:
        objlist.append(alpha * V.loc[int(p0), "weight"])
    for pi in [x for x in pois if x != pN]:  # from
        for pj in [y for y in pois if y != p0]:  # to
            if withNodeWeight == True:
                objlist.append(
                    visit_vars[pi][pj]
                    * (
                        alpha * V.loc[int(pj), "weight"]
                        + beta * E.loc[int(pi), int(pj)]
                    )
                )
            else:
                objlist.append(visit_vars[pi][pj] * E.loc[int(pi), int(pj)])
    pb += pulp.lpSum(objlist), "Objective"

    # add constraints, each constraint should be in ONE line
    pb += pulp.lpSum([visit_vars[p0][pj] for pj in pois if pj != p0]) == 1, "StartAt_p0"
    pb += pulp.lpSum([visit_vars[pi][pN] for pi in pois if pi != pN]) == 1, "EndAt_pN"
    if p0 != pN:
        pb += pulp.lpSum([visit_vars[pi][p0] for pi in pois]) == 0, "NoIncoming_p0"
        pb += pulp.lpSum([visit_vars[pN][pj] for pj in pois]) == 0, "NoOutgoing_pN"
    pb += (
        pulp.lpSum(
            [visit_vars[pi][pj] for pi in pois if pi != pN for pj in pois if pj != p0]
        )
        == L - 1,
        "Length",
    )
    for pk in [x for x in pois if x not in {p0, pN}]:
        pb += (
            pulp.lpSum([visit_vars[pi][pk] for pi in pois if pi != pN])
            == pulp.lpSum([visit_vars[pk][pj] for pj in pois if pj != p0]),
            "ConnectedAt_" + pk,
        )
        pb += (
            pulp.lpSum([visit_vars[pi][pk] for pi in pois if pi != pN]) <= 1,
            "Enter_" + pk + "_AtMostOnce",
        )
        pb += (
            pulp.lpSum([visit_vars[pk][pj] for pj in pois if pj != p0]) <= 1,
            "Leave_" + pk + "_AtMostOnce",
        )
    for pi in [x for x in pois if x != p0]:
        for pj in [y for y in pois if y != p0]:
            pb += (
                dummy_vars[pi] - dummy_vars[pj] + 1
                <= (N - 1) * (1 - visit_vars[pi][pj]),
                "SubTourElimination_" + pi + "_" + pj,
            )

    # solve problem: solver should be available in PATH
    solver = pulp.PULP_CBC_CMD(
        msg=0, options=["-threads", str(n_jobs), "-strategy", "1", "-maxIt", "2000000"]
    )
    pb.solve(solver)
    visit_mat = pd.DataFrame(
        data=np.zeros((len(pois), len(pois)), dtype=np.float64),
        index=pois,
        columns=pois,
    )
    for pi in pois:
        for pj in pois:
            visit_mat.loc[pi, pj] = visit_vars[pi][pj].varValue

    # build the recommended trajectory
    recseq = [p0]
    while True:
        pi = recseq[-1]
        pj = visit_mat.loc[pi].idxmax()
        assert round(visit_mat.loc[pi, pj]) == 1
        recseq.append(pj)
        if pj == pN:
            return [int(x) for x in recseq]


def find_ILP_at_K(
    V: pd.DataFrame,
    E: pd.DataFrame,
    ps: int,
    pe: int,
    L: int,
    edgs: List[List[int]] = [],
    withNodeWeight=False,
    alpha=0.5,
    n_jobs: int = 4,
) -> List[int]:
    assert isinstance(V, pd.DataFrame)
    assert isinstance(E, pd.DataFrame)
    assert ps in V.index
    assert pe in V.index
    assert 2 < L <= V.index.shape[0]
    if withNodeWeight == True:
        assert 0 < alpha < 1
    beta = 1 - alpha

    p0 = str(ps)
    pN = str(pe)
    N = V.index.shape[0]

    # REF: pythonhosted.org/PuLP/index.html
    pois = [str(p) for p in V.index]  # create a string list for each POI
    pb = pulp.LpProblem("MostLikelyTraj", pulp.LpMaximize)  # create problem
    # visit_i_j = 1 means POI i and j are visited in sequence
    visit_vars = pulp.LpVariable.dicts("visit", (pois, pois), 0, 1, pulp.LpInteger)
    # a dictionary contains all dummy variables
    dummy_vars = pulp.LpVariable.dicts(
        "u", [x for x in pois if x != p0], 2, N, pulp.LpInteger
    )

    # add objective
    objlist = []
    if withNodeWeight == True:
        objlist.append(alpha * V.loc[int(p0), "weight"])
    for pi in [x for x in pois if x != pN]:  # from
        for pj in [y for y in pois if y != p0]:  # to
            if withNodeWeight == True:
                objlist.append(
                    visit_vars[pi][pj]
                    * (
                        alpha * V.loc[int(pj), "weight"]
                        + beta * E.loc[int(pi), int(pj)]
                    )
                )
            else:
                objlist.append(visit_vars[pi][pj] * E.loc[int(pi), int(pj)])
    pb += pulp.lpSum(objlist), "Objective"

    # add constraints, each constraint should be in ONE line
    pb += pulp.lpSum([visit_vars[p0][pj] for pj in pois if pj != p0]) == 1, "StartAt_p0"
    pb += pulp.lpSum([visit_vars[pi][pN] for pi in pois if pi != pN]) == 1, "EndAt_pN"
    if p0 != pN:
        pb += pulp.lpSum([visit_vars[pi][p0] for pi in pois]) == 0, "NoIncoming_p0"
        pb += pulp.lpSum([visit_vars[pN][pj] for pj in pois]) == 0, "NoOutgoing_pN"
    pb += (
        pulp.lpSum(
            [visit_vars[pi][pj] for pi in pois if pi != pN for pj in pois if pj != p0]
        )
        == L - 1,
        "Length",
    )
    for pk in [x for x in pois if x not in {p0, pN}]:
        pb += (
            pulp.lpSum([visit_vars[pi][pk] for pi in pois if pi != pN])
            == pulp.lpSum([visit_vars[pk][pj] for pj in pois if pj != p0]),
            "ConnectedAt_" + pk,
        )
        pb += (
            pulp.lpSum([visit_vars[pi][pk] for pi in pois if pi != pN]) <= 1,
            "Enter_" + pk + "_AtMostOnce",
        )
        pb += (
            pulp.lpSum([visit_vars[pk][pj] for pj in pois if pj != p0]) <= 1,
            "Leave_" + pk + "_AtMostOnce",
        )
    for pi in [x for x in pois if x != p0]:
        for pj in [y for y in pois if y != p0]:
            pb += (
                dummy_vars[pi] - dummy_vars[pj] + 1
                <= (N - 1) * (1 - visit_vars[pi][pj]),
                "SubTourElimination_" + pi + "_" + pj,
            )

    # exclude existing solutions given `edgs`
    product_vars = pulp.LpVariable.dicts(
        "prodY", (range(len(edgs))), 0, 1, pulp.LpInteger
    )
    for k in range(len(edgs)):
        c1 = (
            len(edgs[k])
            - 1
            - pulp.lpSum([visit_vars[f"{i}"][f"{j}"] for (i, j) in edgs[k]])
            + product_vars[k]
            >= 0
        )
        pb += c1
        for i, j in edgs[k]:
            c2 = visit_vars[f"{i}"][f"{j}"] - product_vars[k] >= 0
            pb += c2
        c3 = product_vars[k] == 0
        pb += c3

    # solve problem: solver should be available in PATH
    solver = pulp.PULP_CBC_CMD(
        msg=0, options=["-threads", str(n_jobs), "-strategy", "1", "-maxIt", "2000000"]
    )
    pb.solve(solver)
    visit_mat = pd.DataFrame(
        data=np.zeros((len(pois), len(pois)), dtype=np.float64),
        index=pois,
        columns=pois,
    )
    for pi in pois:
        for pj in pois:
            visit_mat.loc[pi, pj] = visit_vars[pi][pj].varValue

    # build the recommended trajectory
    recseq = [p0]
    while True:
        pi = recseq[-1]
        pj = visit_mat.loc[pi].idxmax()
        # assert round(visit_mat.loc[pi, pj]) == 1
        if round(visit_mat.loc[pi, pj]) != 1:
            return False, []
        else:
            recseq.append(pj)
            if pj == pN:
                return True, [int(x) for x in recseq]
