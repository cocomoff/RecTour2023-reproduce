# 1. Preparing data

We need to prepare metadata to generate extended datasets. In addition, to compare experimental results reported in previous work with those obtained by re-implemented baseline methods, we also need to download public datasets.

## 1. Download metadata

If you want to run our reproduced programs (e.g., generating data, run simple baseline methods), you need to either

1. do pre-processing YFCC100m metadata by yourself, or
2. download pre-processed meta files (`new-meta.tar.gz`) from `https://drive.google.com/file/d/1eoRS3tfJMX7oamEz9q4yWnLt4PZ5L28K/view?usp=sharing` and decompress `.tar.gz` in the directory `new-meta`.

Note that the above Google Drive link is only valid during the reviewing process.

## 2. Download public datasets

We require public datasets in both Format-IJCAI2015 and Format-CIKM2016. The links for these datasets are:

- (IJCAI2015 dataset): https://sites.google.com/site/limkwanhui/datacode#ijcai15
- (CIKM2016 dataset): https://bitbucket.org/d-chen/tour-cikm16/src/master/data/

The directory `public-data/` contains modified data from the above public datasets. We encourages users of these datasets to cite the following papers:

- Kwan Hui Lim, Jeffrey Chan, Christopher Leckie and Shanika Karunasekera. "Personalized Tour Recommendation based on User Interests and Points of Interest Visit Durations". IJCAI2015.
- Dawei Chen, Cheng Soon Ong and Lexing Xie. "Learning Points and Routes to Recommend Trajectories". CIKM2016.


Note that `modified data` means we download raw data from the above two links and edit them as follows.

- Fixed delimiter (`;`, `,`) are unified.
- Column names (e.g., `poiLat` and `lat`) are unified.
- Spatial error in Osaka data (latitude and longitude of PoiID 26 is incorrect) is removed.