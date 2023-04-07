import argparse
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from myutil import city_names


def main(args) -> None:
    city = args.city

    # data
    fn_visit = f"extended-data/Format-IJCAI2015/userVisits-{city}.csv"
    fn_output = f"extended-data/Format-CIKM2016/traj-{city}.csv"
    df_visit = pd.read_csv(fn_visit)

    # remove negative time stamp
    df_visit = df_visit[df_visit.datetaken > 0]

    # output dataframe
    df_output = pd.DataFrame(
        {
            "userID": pd.Series(dtype="str"),
            "trajID": pd.Series(dtype="int"),
            "poiID": pd.Series(dtype="int"),
            "startTime": pd.Series(dtype="int"),
            "endTime": pd.Series(dtype="int"),
            "#photo": pd.Series(dtype="int"),
            "trajLen": pd.Series(dtype="int"),
            "poiDuration": pd.Series(dtype="int"),
        }
    )

    dfg = df_visit.groupby(["uid", "seqID"])
    for idc, (_, dfkey) in enumerate(dfg):
        dfkey.sort_values("datetaken", inplace=True)
        df_seqID = pd.DataFrame(
            {
                "userID": pd.Series(dtype="str"),
                "trajID": pd.Series(dtype="int"),
                "poiID": pd.Series(dtype="int"),
                "startTime": pd.Series(dtype="int"),
                "endTime": pd.Series(dtype="int"),
                "#photo": pd.Series(dtype="int"),
                "trajLen": pd.Series(dtype="int"),
                "poiDuration": pd.Series(dtype="int"),
            }
        )

        ids = dfkey["poiID"].tolist()
        pois = list(set(ids))

        for p in pois:
            dfp = dfkey[dfkey.poiID == p]
            dfps = dfp.sort_values("datetaken")
            st = dfps.iloc[0].datetaken
            et = dfps.iloc[-1].datetaken
            duration = et - st

            row = {
                "userID": dfps.iloc[0].uid,
                "trajID": idc + 1,
                "poiID": dfps.iloc[0].poiID,
                "startTime": st,
                "endTime": et,
                "#photo": dfps.shape[0],
                "trajLen": len(pois),
                "poiDuration": duration,
            }
            df_seqID.loc[-1] = row
            df_seqID.reset_index(drop=True, inplace=True)

        # merge
        df_output = pd.concat([df_output, df_seqID])

    df_output.sort_values("endTime", inplace=True)
    df_output.sort_values("trajID", inplace=True)
    df_output.reset_index(drop=True, inplace=True)
    df_output.to_csv(fn_output, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-city", type=str, default="Osak")
    args = parser.parse_args()
    main(args)
