#!/bin/zsh

# public
for c in Edin Glas Melb Osak Toro
do
    python src/tour/visualize/plot-POI.py \
            -filename=./public-data/POI/POI-${c}.csv \
            -outputname=./figures/POI/public-${c}.png
done

# (POI Ext1)
python src/tour/visualize/plot-POI.py \
        -filename=./extended-data/POI/POI-HC-Kyot.csv \
        -outputname=./figures/POI/HC-Kyot.png

# (POI Ext2)
for c in NYC TKY
do
    python src/tour/visualize/plot-POI.py \
            -filename=./extended-data/POI/POI-4sq-${c}.csv \
            -outputname=./figures/POI/4sq-${c}.png
done

# (POI Ext3)
for c in beppu fukuoka hiroshima kanazawa kumamoto kyoto matsumoto nagasaki naha osaka tokyo
do
    python src/tour/visualize/plot-POI.py \
            -filename=./extended-data/POI/POI-${c}.csv \
            -outputname=./figures/POI/ext-${c}.png
done