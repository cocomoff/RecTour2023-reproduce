import pandas as pd
import matplotlib.pyplot as plt
import argparse


def plot_poi_scatter(name: str, oname: str) -> None:
    df = pd.read_csv(name, delimiter=",", index_col=0)
    f = plt.figure(figsize=(5, 5))
    a = f.gca()
    df.plot.scatter(x="poiLon", y="poiLat", ax=a)
    plt.title(f"data: {name}")
    plt.tight_layout()
    plt.savefig(oname, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-filename", type=str, default="./public-data/POI/POI-Edin.csv")
    parser.add_argument("-outputname", type=str, default="./figures/POI/Edin.png")
    args = parser.parse_args()
    plot_poi_scatter(args.filename, args.outputname)
