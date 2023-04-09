import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from typing import List


def train_kmeans(
    poi_all: pd.DataFrame,
    indices: List[int],
    nclusters: int,
    rs: int = 0,
    show_fig: bool = False,
) -> pd.DataFrame:
    """
    K-means-based factorization of POIs by their locations (Lon, Lat).
    """

    # Applying K-means
    X = poi_all.loc[indices, ["poiLon", "poiLat"]]
    kmeans = KMeans(n_clusters=nclusters, random_state=rs)
    kmeans.fit(X)

    # Predict labels and generate information
    clusters = kmeans.predict(X)
    POI_CLUSTER_LIST = sorted(np.unique(clusters))
    POI_CLUSTERS = pd.DataFrame(data=clusters, index=indices)
    POI_CLUSTERS.index.name = "poiID"
    POI_CLUSTERS.rename(columns={0: "clusterID"}, inplace=True)
    POI_CLUSTERS["clusterID"] = POI_CLUSTERS["clusterID"].astype(np.int64)

    # visualize
    if show_fig:
        # scattering
        diff = (
            poi_all.loc[indices, ["poiLon", "poiLat"]].max()
            - poi_all.loc[indices, ["poiLon", "poiLat"]].min()
        )
        ratio = diff["poiLon"] / diff["poiLat"]
        height = 6
        width = int(round(ratio) * height)
        plt.figure(figsize=[width, height])
        plt.scatter(
            poi_all.loc[indices, "poiLon"],
            poi_all.loc[indices, "poiLat"],
            c=clusters,
            s=50,
        )
        plt.tight_layout()
        plt.show()

    return POI_CLUSTERS
