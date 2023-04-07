import glob
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from os.path import exists
from myutil import dG, city_names
from tqdm import tqdm
import dill


import argparse


def main(args, HOURS=8) -> None:
    df_poi = pd.read_csv(args.poiname, comment="#", delimiter=",")

    # all data (pre-processed `dill` file) and sort data by time
    data_all = dill.load(open(f"extended-data/distance/{args.city}.dill", "rb"))
    df_all = pd.DataFrame.from_records(data_all)
    df_all.sort_values(["datetaken", "photoid"], inplace=True)
    df_all.reset_index(inplace=True)

    print(f"org data: {df_all.shape}")

    if (
        not exists(f"extended-data/distance-mapping/{args.city}-dist.dill")
        or args.overwrite
    ):
        list_df = []

        # Split by user (uid)
        dfgu = df_all.groupby("uid")
        for _, df in tqdm(dfgu):
            # keep distance < 0.2 (=dG) [km]
            rem_rows = []
            list_pois = []
            list_themes = []
            for idr, row in df.iterrows():
                lat, lon = row.latitude, row.longitude
                min_row = None
                min_dist = float("inf")
                for _, rowj in df_poi.iterrows():
                    lat_j = rowj.poiLat
                    lon_j = rowj.poiLon
                    dd = dG(lat, lon, lat_j, lon_j)
                    if dd < min_dist:
                        min_dist = dd
                        min_row = rowj
                if min_dist < args.dG:
                    list_pois.append(min_row.poiID)
                    list_themes.append(min_row.theme)
                    rem_rows.append(row)

            if len(rem_rows) > 0:
                df_new_key = pd.DataFrame.from_records(rem_rows)
                df_new_key.drop("index", inplace=True, axis=True)
                df_new_key["poiID"] = list_pois
                df_new_key["poiTheme"] = list_themes
                list_df.append(df_new_key)

        # save
        with open(f"extended-data/distance-mapping/{args.city}-dist.dill", "wb") as f:
            dill.dump(list_df, f)

    else:
        list_df = dill.load(
            open(f"extended-data/distance-mapping/{args.city}-dist.dill", "rb")
        )

    # Generate Data Frame (Format-IJCAI2015)
    df_all = pd.concat(list_df)
    df_all.reset_index(inplace=True)
    df_all.drop("index", axis=1, inplace=True)
    print(f"data frame size: {df_all.shape}")

    # Add POI Frequency
    dict_poi_freq = dict(df_all.poiID.value_counts())
    series_freq = df_all.poiID.map(lambda x: dict_poi_freq[x])
    df_all["poiFreq"] = series_freq

    # Fix datetaken format to timestamp value
    series_date = df_all.datetaken.map(
        lambda x: int(datetime.fromisoformat(x.split(".")[0]).timestamp())
    )
    df_all["datetaken"] = series_date

    # Split (up to 8h)
    dfgu = df_all.groupby("uid")
    all_new_index = []
    for _, (key, df) in enumerate(dfgu):
        list_ts = list(map(lambda x: datetime.fromtimestamp(x), df.datetaken.tolist()))

        split_index = []
        current = [0]
        prev = list_ts[0]
        for i in range(1, len(list_ts)):
            now = list_ts[i]
            diff = now - prev
            if diff.seconds < HOURS * 60 * 60 and diff.days == 0:
                prev = now
                current.append(i)
            else:
                # split
                split_index.append(current)
                current = [i]
                prev = list_ts[i]
        else:
            if current:
                split_index.append(current)

        new_index = [df.index[elem] for elem in split_index]
        all_new_index += new_index

    # Assign sequence ID (seqID)
    for seqID, i in enumerate(all_new_index):
        df_all.loc[i, "seqID"] = int(seqID + 1)
    df_all.seqID = df_all.seqID.astype(int)

    # Modify column name for consistency (w.r.t. public dataN)
    df_all.rename(
        columns={"photoid": "photoID", "uid": "userID", "datetaken": "dateTaken"},
        inplace=True,
    )

    # Clean up data frame of Visits data
    df_main = df_all[
        ["photoID", "userID", "dateTaken", "poiID", "poiTheme", "poiFreq", "seqID"]
    ]

    # Save files
    fn_output = f"extended-data/Format-IJCAI2015/userVisits-{args.city}.csv"
    df_main.to_csv(fn_output, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-city", type=str, default="Osak")
    parser.add_argument("-poiname", type=str, default="public-data/POI/POI-Osak.csv")
    parser.add_argument("-dG", type=float, default=0.2)
    parser.add_argument("-overwrite", action="store_true")
    args = parser.parse_args()
    main(args)
