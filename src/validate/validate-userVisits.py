import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


def main(args) -> None:
    city = args.city

    # data1 (public)
    fn_path1 = f"public-data/userVisits/userVisits-{city}.csv"
    df1 = pd.read_csv(fn_path1)

    # data2 (generated)
    fn_path2 = f"extended-data/Format-IJCAI2015/userVisits-{city}.csv"
    df2 = pd.read_csv(fn_path2)

    # size
    print(
        f"{city:>8s},{df1.userID.nunique():>5d},{df1.shape[0]:>5d},{df1.seqID.max():>5d}"
    )
    print(
        f"{'(ours)':>8s},{df2.userID.nunique():>5d},{df2.shape[0]:>5d},{df2.seqID.max():>5d}"
    )

    # POI Visits histogram
    M = df1.poiID.max()
    h1 = np.zeros(M + 1)
    h2 = np.zeros(M + 1)

    for k, _ in df1.groupby(["poiID", "poiFreq"]):
        h1[k[0]] = k[1]
    for k, _ in df2.groupby(["poiID", "poiFreq"]):
        h2[k[0]] = k[1]

    f = plt.figure(figsize=(8, 3))
    a = f.gca()
    xseq = np.array(range(M + 1))
    a.bar(x=xseq - 0.2, height=h1, width=0.4, label="IJCAI15")
    a.bar(x=xseq + 0.2, height=h2, width=0.4, label="Reproduced")
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

    # Timestamp histograms
    h1 = []
    h2 = []

    for k, d in df1.groupby("dateTaken"):
        h1.append(k)
    for k, d in df2.groupby("dateTaken"):
        h2.append(k)

    f = plt.figure(figsize=(8, 3))
    a = f.gca()
    xseq = np.array(range(M + 1))
    a.hist([h1, h2], bins=300, label=["IJCAI15", "Reproduced"])
    a.legend(loc="upper left")
    a.set_title(f"{city}")
    a.set_xlabel("datetaken")
    a.set_xlim(1e9, max(max(h1), max(h2)))
    a.set_ylabel("# photos")
    plt.tight_layout()
    plt.savefig(
        f"figures/validate/timestamp/timehist-{city}.png",
        bbox_inches="tight",
        facecolor="w",
        dpi=120,
    )
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-city", type=str, default="Osak")
    args = parser.parse_args()
    main(args)
