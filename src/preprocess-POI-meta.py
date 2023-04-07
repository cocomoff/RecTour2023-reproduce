import argparse
import pickle
import glob
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from os.path import exists
from tqdm import tqdm
import json
import gzip
import dill
from myutil import city_names


def main(args) -> None:
    df_poi = pd.read_csv(args.poiname, comment="#", delimiter=",")
    fn = f"extended-data/distance/{args.city}.dill"

    if not exists(fn):
        min_lat = df_poi.poiLat.min()
        max_lat = df_poi.poiLat.max()
        min_lon = df_poi.poiLon.min()
        max_lon = df_poi.poiLon.max()

        # Remain meta data whose distances to POIs rectangles are <= `eps`
        eps = args.eps
        photos = []
        for line in tqdm(sorted(glob.glob("new-meta/*.gz"))):
            with gzip.open(line, "tr") as f:
                for line_j in f:
                    line_j = line_j.strip()
                    data = json.loads(line_j)
                    lat = data["latitude"]
                    lon = data["longitude"]

                    f1 = min_lat - eps <= lat and lat <= max_lat + eps
                    f2 = min_lon - eps <= lon and lon <= max_lon + eps
                    f3 = data["accuracy"] == 16
                    if f1 and f2 and f3:
                        photos.append(data)

        # save
        with open(fn, "wb") as f:
            dill.dump(photos, f)
    else:
        print(f"{fn} already exists.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-city", type=str, default="Osak")
    parser.add_argument("-poiname", type=str, default="public-data/POI/POI-Osak.csv")
    parser.add_argument("-dG", type=float, default=0.2)
    parser.add_argument("-eps", type=float, default=0.01)
    args = parser.parse_args()
    main(args)
