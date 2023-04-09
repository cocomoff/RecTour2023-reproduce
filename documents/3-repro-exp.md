# 3. Re-producing previous experimental results

In [#2](2-repro-data.md), we explained re-production scripts to generate (extended) travel log data. Next, we explain how to re-produce existing research results using baseline solvers (Popularity and Markov@K). Some implementations are from [CIKM2016 repository](https://bitbucket.org/d-chen/tour-cikm16/src/master/).


## 3-1. Solvers and utility functions

Baseline solves are implemented in `src/tour/*`. Here we implemented for reproducibility `POP` (Popularity) and `ILP` (MarkovPath). Based on the two baseline optimizers, we also implemented `@k` variants (Popularity@k and MarkovPath@k).

Run `src/experiments/example.py` to check how our solvers work in Osaka and Glasgow, where experiment configurations are given in `config/*.json` files (see `osak.json`) for example.


## 3-2. Experiments for reproducing previous results

To reproduce experiments reported in previous work (e.g., Lim et al. in IJCAI2015 or Chen et al. CIKM2016), we try three approaches (corresponding to (Q1) and (Q2) columns in Table 6; Reproduction Validation).

For the purpose, we use two data (1) public data (in `public-data/POI-CIKM2016` and `public-data/traj`) and (2) reproduced data (in `public-data/POI-CKM2016` and `extended-data/Format-CIKM2016`). Note that experiments using (1) is for (Q1) and those using (2) is for (Q2).

Here we prepare the two config files in Osaka; `config/osak.json` for (1) and `config/reproduced/osak.json` for (2), and the same files are prepared for Glasgow as well. The experiment script is `src/experiments/reproduce-Q1-and-Q2.py`.

```
# run Osaka and Glasgow using four config files.
python src/experiments/reproduce-Q1-and-Q2.py
```

Resulted log files in Osaka means:

- results/logs/log-Osak.csv (Q1)
- results/logs/log-reproduced-Osaka.csv (Q2)

After collecting those results in five cities and results already reported in Chen et al. (CIKM2016), we can obtain Table 6 (maybe some differences can be observed due to differences of (1) computational environments, (2) some (possibly hidden) random seeds, and (3) combinatorial solvers).

## 3-3. Experiments using extended datasets

To use extended datasets such as Kumamoto, we just write a config file as follows (see `config/extended/kumamoto.json` as well).

```
# run Kumamoto
python src/experiments/extend-kumamoto.py
```