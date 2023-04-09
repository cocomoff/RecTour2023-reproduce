import itertools
import numpy as np
import pandas as pd
from scipy.linalg import kron
from typing import List, Dict, Set
from ..util.utility import extract_poi_cats_list
from ..util.logbins import extract_logbins
from ..util.neighbors import train_kmeans


def normalise_transmat(transmat_cnt: pd.DataFrame) -> pd.DataFrame:
    transmat = transmat_cnt.copy()
    assert isinstance(transmat, pd.DataFrame)
    for row in range(transmat.index.shape[0]):
        rowsum = np.sum(transmat.iloc[row] + 1)
        assert rowsum > 0
        transmat.iloc[row] = (transmat.iloc[row] + 1) / rowsum
    return transmat


def gen_transmat_cat(
    trajid_list: List[int],
    traj_dict: Dict[int, List[int]],
    df_poi: pd.DataFrame,
    poi_cats: List[str],
    target: str = "poiCat",
) -> pd.DataFrame:
    transmat_cat_cnt = pd.DataFrame(
        data=np.zeros((len(poi_cats), len(poi_cats)), dtype=np.float64),
        columns=poi_cats,
        index=poi_cats,
    )
    for tid in trajid_list:
        t = traj_dict[tid]
        if len(t) > 1:
            # print(tid, t)
            for pi in range(len(t) - 1):
                p1 = t[pi]
                p2 = t[pi + 1]
                assert p1 in df_poi.index and p2 in df_poi.index
                cat1 = df_poi.loc[p1, target]
                cat2 = df_poi.loc[p2, target]
                transmat_cat_cnt.loc[cat1, cat2] += 1
    return normalise_transmat(transmat_cat_cnt)


def gen_transmat_cluster(
    trajid_list: List[int],
    traj_dict: Dict[int, List[int]],
    df_poi: pd.DataFrame,
    df_cluster: pd.DataFrame,
    target: str = "clusterID",
) -> pd.DataFrame:
    nclusters = len(df_cluster["clusterID"].unique())
    transmat_ng_count = pd.DataFrame(
        data=np.zeros((nclusters, nclusters), dtype=np.float64),
        columns=np.arange(nclusters),
        index=np.arange(nclusters),
    )
    for tid in trajid_list:
        t = traj_dict[tid]
        if len(t) > 1:
            # print(tid, t)
            for pi in range(len(t) - 1):
                p1 = t[pi]
                p2 = t[pi + 1]
                assert p1 in df_poi.index and p2 in df_poi.index
                c1 = df_cluster.loc[p1, target]
                c2 = df_cluster.loc[p2, target]
                transmat_ng_count.loc[c1, c2] += 1
    return normalise_transmat(transmat_ng_count)


def gen_transmat_target(
    trajid_list: List[int],
    traj_dict: Dict[int, List[int]],
    poi_info: pd.DataFrame,
    logbin: pd.Series,
    target: str,
) -> pd.DataFrame:
    nbins = len(logbin) - 1
    transmat_count = pd.DataFrame(
        data=np.zeros((nbins, nbins), dtype=np.float64),
        columns=np.arange(1, nbins + 1),
        index=np.arange(1, nbins + 1),
    )
    for tid in trajid_list:
        t = traj_dict[tid]
        if len(t) > 1:
            for pi in range(len(t) - 1):
                p1 = t[pi]
                p2 = t[pi + 1]
                assert p1 in poi_info.index and p2 in poi_info.index
                l1 = poi_info.loc[p1, target]
                l2 = poi_info.loc[p2, target]
                pc1, pc2 = np.digitize([l1, l2], logbin)
                transmat_count.loc[pc1, pc2] += 1
    return normalise_transmat(transmat_count)


def gen_poi_logtransmat(
    trajid_list: List[int],
    traj_dict: Dict[int, List[int]],
    poi_info_all: pd.DataFrame,
    BIN_CLUSTER: int = 5,
    LOG_ZERO: int = -1000,
) -> None:
    poi_set: Set[int] = set(poi_info_all.index)
    poi_train = sorted(poi_info_all.index)
    poi_cat_list = extract_poi_cats_list(poi_info_all, poi_train)

    # Normal plot: poiCat
    target = "poiCat"
    transmat_cat = gen_transmat_cat(
        trajid_list, traj_dict, poi_info_all, poi_cats=poi_cat_list, target=target
    )

    # Logbin plot: popularity
    target = "popularity"
    series_pop, logbins_pop = extract_logbins(
        poi_info_all, poi_train, nbins=BIN_CLUSTER, target=target
    )
    # basic_fact_figures(city, series_pop, logbins_pop)

    transmat_pop = gen_transmat_target(
        trajid_list, traj_dict, poi_info_all, logbins_pop, target=target
    )

    # Logbin plot: Visits
    target = "nVisit"
    series_visits, logbins_visit = extract_logbins(
        poi_info_all, poi_train, nbins=BIN_CLUSTER, target=target
    )
    # basic_fact_figures(city, series_visits, logbins_visits)
    transmat_visit = gen_transmat_target(
        trajid_list, traj_dict, poi_info_all, logbins_visit, target=target
    )

    # Logbin plot: avgDurations
    target = "avgDuration"
    series_duration, logbins_duration = extract_logbins(
        poi_info_all, poi_train, nbins=BIN_CLUSTER, target=target
    )
    # basic_fact_figures(city, series_duration, logbins_duration, label=target)
    transmat_duration = gen_transmat_target(
        trajid_list, traj_dict, poi_info_all, logbins_duration, target=target
    )

    # K-means
    poi_clusters = train_kmeans(
        poi_info_all, poi_train, nclusters=BIN_CLUSTER, show_fig=False
    )

    # Normal plot: k-Means clustering label
    target = "clusterID"
    transmat_neighbor = gen_transmat_cluster(
        trajid_list, traj_dict, poi_info_all, poi_clusters, target=target
    )

    # Kronecker product
    transmat_ix = list(
        itertools.product(
            transmat_cat.index,
            transmat_pop.index,
            transmat_visit.index,
            transmat_duration.index,
            transmat_neighbor.index,
        )
    )
    transmat_value = transmat_cat.values
    for transmat in [
        transmat_pop,
        transmat_visit,
        transmat_duration,
        transmat_neighbor,
    ]:
        transmat_value = kron(transmat_value, transmat.values)
    transmat_feature = pd.DataFrame(
        data=transmat_value, index=transmat_ix, columns=transmat_ix
    )

    poi_train = sorted(poi_set)
    feature_names = ["poiCat", "popularity", "nVisit", "avgDuration", "clusterID"]
    poi_features = pd.DataFrame(
        data=np.zeros((len(poi_train), len(feature_names))),
        columns=feature_names,
        index=poi_train,
    )
    poi_features.index.name = "poiID"
    poi_features["poiCat"] = poi_info_all.loc[poi_train, "poiCat"]
    poi_features["popularity"] = np.digitize(
        poi_info_all.loc[poi_train, "popularity"], logbins_pop
    )
    poi_features["nVisit"] = np.digitize(
        poi_info_all.loc[poi_train, "nVisit"], logbins_visit
    )
    poi_features["avgDuration"] = np.digitize(
        poi_info_all.loc[poi_train, "avgDuration"], logbins_duration
    )
    poi_features["clusterID"] = poi_clusters.loc[poi_train, "clusterID"]

    # shrink the result of Kronecker product and deal with POIs with the same features
    poi_logtransmat = pd.DataFrame(
        data=np.zeros((len(poi_train), len(poi_train)), dtype=np.float64),
        columns=poi_train,
        index=poi_train,
    )
    for p1 in poi_logtransmat.index:
        rix = tuple(poi_features.loc[p1])
        for p2 in poi_logtransmat.columns:
            cix = tuple(poi_features.loc[p2])
            value_ = transmat_feature.loc[(rix,), (cix,)]
            poi_logtransmat.loc[p1, p2] = value_.values[0, 0]

    # group POIs with the same features
    features_dup = dict()
    for poi in poi_features.index:
        key = tuple(poi_features.loc[poi])
        if key in features_dup:
            features_dup[key].append(poi)
        else:
            features_dup[key] = [poi]

    # deal with POIs with the same features
    for feature in sorted(features_dup.keys()):
        n = len(features_dup[feature])
        if n > 1:
            group = features_dup[feature]
            v1 = poi_logtransmat.loc[
                group[0], group[0]
            ]  # transition value of self-loop of POI group

            # divide incoming transition value (i.e. unnormalised transition probability) uniformly among group members
            for poi in group:
                poi_logtransmat[poi] /= n

            # outgoing transition value has already been duplicated (value copied above)

            # duplicate & divide transition value of self-loop of POI group uniformly among all outgoing transitions,
            # from a POI to all other POIs in the same group (excluding POI self-loop)
            v2 = v1 / (n - 1)
            for pair in itertools.permutations(group, 2):
                poi_logtransmat.loc[pair[0], pair[1]] = v2

    # normalise each row
    for p1 in poi_logtransmat.index:
        poi_logtransmat.loc[p1, p1] = 0
        rowsum = poi_logtransmat.loc[p1].sum()
        assert rowsum > 0
        logrowsum = np.log10(rowsum)
        for p2 in poi_logtransmat.columns:
            if p1 == p2:
                poi_logtransmat.loc[p1, p2] = LOG_ZERO  # deal with log(0) explicitly
            else:
                poi_logtransmat.loc[p1, p2] = (
                    np.log10(poi_logtransmat.loc[p1, p2]) - logrowsum
                )

    return poi_logtransmat
