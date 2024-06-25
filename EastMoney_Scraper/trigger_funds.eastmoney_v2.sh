#!/bin/bash

# Change to the desired directory
cd /home/app/Desktop/output_china || { echo "Directory change failed"; exit 1; }

# Execute the Python script
python /home/app/Desktop/Pathfinder-Analysis/EastMoney_Scraper/funds.eastmoney_v2.py || { echo "Script execution failed"; exit 1; }
