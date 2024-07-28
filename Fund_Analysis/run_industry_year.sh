#!/bin/bash

# Define the start date
start_year=$1
start_date=$start_year-01-01

# Define the end date (1 year later)
end_date=$(date -I -d "$start_date + 1 year")

# Define input and output directories
input_dir="/home/app/Desktop/output_china"
output_dir="/home/app/Desktop/industry_out/"$start_year

# Loop through each day within the date range
current_date="$start_date"
while [ "$current_date" != "$end_date" ]; do
    echo "Running script for date: $current_date"
    python industry.py --input=$input_dir --output=$output_dir --date=$current_date --year=$start_year
    current_date=$(date -I -d "$current_date + 1 day")
done

echo "Completed running script for one year."