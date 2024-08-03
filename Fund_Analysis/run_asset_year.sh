#!/bin/bash

start_year=$1
for QUARTER in {1..4}
do
    echo "Processing year $start_year, quarter $QUARTER..."
    python asset.py --input=/home/app/Desktop/output_china --output=/home/app/Desktop/asset_out --year="$start_year" --quarter="$QUARTER"
done