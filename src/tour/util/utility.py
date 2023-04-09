import pandas as pd
import numpy as np
from typing import List


def calc_dist_vec(
    longitudes1: np.ndarray,
    latitudes1: np.ndarray,
    longitudes2: np.ndarray,
    latitudes2: np.ndarray,
) -> np.ndarray:
    """
    Calculate the distance (unit: km) between two places on earth, vectorised.

    See
    - The haversine formula, en.wikipedia.org/wiki/Great-circle_distance
    - Mean earth radius, en.wikipedia.org/wiki/Earth_radius#Mean_radius
    """
    # convert degrees to radians
    lng1 = np.radians(longitudes1)
    lat1 = np.radians(latitudes1)
    lng2 = np.radians(longitudes2)
    lat2 = np.radians(latitudes2)
    radius = 6371.0088

    dlng = np.fabs(lng1 - lng2)
    dlat = np.fabs(lat1 - lat2)
    dist = (
        2
        * radius
        * np.arcsin(
            np.sqrt(
                (np.sin(0.5 * dlat)) ** 2
                + np.cos(lat1) * np.cos(lat2) * (np.sin(0.5 * dlng)) ** 2
            )
        )
    )
    return dist


def extract_traj(tid: int, traj_all: pd.DataFrame) -> pd.DataFrame:
    traj = traj_all[traj_all["trajID"] == tid].copy()
    traj.sort_values(by=["startTime"], ascending=True, inplace=True)
    return traj["poiID"].tolist()


def calc_poi_info(
    trajid_list: List[int], traj_all: pd.DataFrame, poi_all: pd.DataFrame
) -> pd.DataFrame:
    assert len(trajid_list) > 0
    poi_info = traj_all[traj_all["trajID"] == trajid_list[0]][
        ["poiID", "poiDuration"]
    ].copy()
    for i in range(1, len(trajid_list)):
        traj = traj_all[traj_all["trajID"] == trajid_list[i]][["poiID", "poiDuration"]]
        poi_info = pd.concat([poi_info, traj], ignore_index=True)

    poi_info = poi_info.groupby("poiID").agg([np.mean, np.size])
    poi_info.columns = poi_info.columns.droplevel()
    poi_info.reset_index(inplace=True)
    poi_info.rename(columns={"mean": "avgDuration", "size": "nVisit"}, inplace=True)
    poi_info.set_index("poiID", inplace=True)
    poi_info["poiCat"] = poi_all.loc[poi_info.index, "poiCat"]
    poi_info["poiLon"] = poi_all.loc[poi_info.index, "poiLon"]
    poi_info["poiLat"] = poi_all.loc[poi_info.index, "poiLat"]

    # POI popularity: the number of distinct users that visited the POI
    pop_df = traj_all[traj_all["trajID"].isin(trajid_list)][["poiID", "userID"]].copy()
    pop_df = pop_df.groupby("poiID").agg(pd.Series.nunique)
    pop_df.rename(columns={"userID": "nunique"}, inplace=True)
    poi_info["popularity"] = pop_df.loc[poi_info.index, "nunique"]

    return poi_info.copy()


def extract_poi_cats_list(df: pd.DataFrame, indices: List[int]) -> List[str]:
    # category list
    poi_cats = df.loc[indices, "poiCat"].unique().tolist()
    poi_cats.sort()
    return poi_cats
