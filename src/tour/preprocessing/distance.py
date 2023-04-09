import numpy as np
import pandas as pd
from ..util.utility import calc_dist_vec


def compute_poi_distmat(poi_all: pd.DataFrame) -> pd.DataFrame:
    poi_distmat = pd.DataFrame(
        data=np.zeros((poi_all.shape[0], poi_all.shape[0]), dtype=np.float64),
        index=poi_all.index,
        columns=poi_all.index,
    )

    for ix in poi_all.index:
        poi_distmat.loc[ix] = calc_dist_vec(
            poi_all.loc[ix, "poiLon"],
            poi_all.loc[ix, "poiLat"],
            poi_all["poiLon"],
            poi_all["poiLat"],
        )

    return poi_distmat
