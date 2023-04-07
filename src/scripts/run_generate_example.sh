#!/bin/zsh

# Example of generating datasets for Osak, Glas, and Kumamoto.

# Osak
python generator/preprocess-POI-meta.py -city Osak -poiname public-data/POI/POI-Osak.csv
python generator/generate-Visits.py -city Osak -poiname public-data/POI/POI-Osak.csv
python generator/convert-Visits-Traj.py -city Osak

# Glas
python generator/preprocess-POI-meta.py -city Glas -poiname public-data/POI/POI-Glas.csv
python generator/generate-Visits.py -city Glas -poiname public-data/POI/POI-Glas.csv
python generator/convert-Visits-Traj.py -city Glas


# Kuma
python generator/preprocess-POI-meta.py -city Kumamoto -poiname extended-data/POI/POI-Kumamoto.csv
python generator/generate-Visits.py -city Kumamoto -poiname extended-data/POI/POI-Kumamoto.csv
python generator/convert-Visits-Traj.py -city Kumamoto