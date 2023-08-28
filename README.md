# RecTour2023 Paper; Extending Travel Itinerary Datasets


This anonymized repository is available during the period of the RecSys2023 conference. Please see the contents below as the companion content and our submission if you are interested.


# Documents

The followings are documents.

- [0. Environment](./documents/0-environment.md)
- [1. Preparing data](./documents/1-preparing-data.md)
- [2. Re-producing data](./documents/2-repro-data.md)
- [3. Re-producing previous experimental results](./documents/3-repro-exp.md)


# Structure of repository

The following outline represents the structure of this repository.

- `config/` contains config files for experiments.
- `documents/` contains documents for this repository.
- `extended-data/` contains extended POI data.
- `figures/` contains output images.
- `new-meta/` contains pre-processed metadata (see Fig.1 in our submission).
- `public-data/` contains public travel log data.
- `results/` contains figures and log data.
- `src/` contains program files.
  - `src/generator/` contains tools to process and generated extended travel log data.
  - `src/tour/` contains baseline implementations for travel itinerary recommendations.
- `scripts/` contains batch files to do experiments and/or visualization.
