import argparse
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


def main(args) -> None:
    city = args.city

    # data1 (generated traj)
    fn_path = f"extended-data/Format-CIKM2016/traj-{city}.csv"
    if not os.path.exists(fn_path):
        return
    df = pd.read_csv(fn_path)
    print(f"{city:>8s},{df.userID.nunique()},{df['#photo'].sum()},{df.trajID.max()}")

    M = df.poiID.max()
    h1 = np.zeros(M + 1)
    for idr, row in df.iterrows():
        h1[row.poiID] += row["#photo"]

    f = plt.figure(figsize=(8, 3))
    a = f.gca()
    xseq = np.array(range(M + 1))
    a.bar(x=xseq, height=h1, width=0.4, label="CIKM16")
    a.legend(loc="upper right")
    a.set_title(f"{city}")
    a.set_xlabel("POI ID")
    a.set_ylabel("# visits")
    plt.tight_layout()
    plt.savefig(
        f"figures/validate/visits/hist-{city}.png",
        bbox_inches="tight",
        facecolor="w",
        dpi=120,
    )
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-city", type=str, default="Kumamoto")
    args = parser.parse_args()
    main(args)
